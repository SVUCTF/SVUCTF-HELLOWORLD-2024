import { useCallback } from 'react';
import { useChallengeContext } from '../contexts/ChallengeContext';
import useWebSocket from './useWebSocket';
import { ChallengeInfoMessage, SimulationResultMessage, WorldUpdateMessage, WebSocketResponseUnion } from '../types/challenge';
import { CellUnion } from '../types/wireworld';

const useChallenge = (url: string) => {
    const {
        setChallengeInfo,
        setGridState,
        setIsSimulating,
        setChallengeResult,
    } = useChallengeContext();

    const handleWebSocketMessage = useCallback((data: WebSocketResponseUnion) => {
        switch (data.type) {
            case 'challenge_info':
                handleChallengeInfo(data);
                break;
            case 'world_update':
                handleWorldUpdate(data);
                break;
            case 'simulation_result':
                handleSimulationResult(data);
                break;
            case 'error':
                setChallengeResult({
                    message: data.message,
                    success: false,
                    flag: null
                });
                break;
        }
    }, [setChallengeInfo, setGridState, setIsSimulating, setChallengeResult]);

    const { sendMessage } = useWebSocket(url, handleWebSocketMessage);

    const handleChallengeInfo = useCallback((info: ChallengeInfoMessage) => {
        setChallengeInfo(info);
        setGridState(info.initial_state);
    }, [setChallengeInfo, setGridState]);

    const handleWorldUpdate = useCallback((update: WorldUpdateMessage) => {
        setGridState(update.grid_state);
    }, [setGridState]);

    const handleSimulationResult = useCallback((result: SimulationResultMessage) => {
        setIsSimulating(false);
        setGridState(result.final_state);
        setChallengeResult({
            message: result.success ? 'Challenge completed successfully!' : 'Challenge failed. Try again!',
            success: result.success,
            flag: result.flag
        });
    }, [setIsSimulating, setGridState, setChallengeResult]);

    const startSimulation = useCallback((design: CellUnion[][]) => {
        sendMessage(JSON.stringify({
            type: 'simulate',
            design: design
        }));
        setIsSimulating(true);
        setChallengeResult({
            message: '',
            success: undefined,
            flag: null
        });
    }, [sendMessage, setIsSimulating, setChallengeResult]);

    const resetSimulation = useCallback(() => {
        sendMessage(JSON.stringify({ type: 'reset' }));
        setIsSimulating(false);
        setChallengeResult({
            message: '',
            success: undefined,
            flag: null
        });
    }, [sendMessage, setIsSimulating, setChallengeResult]);

    return {
        startSimulation,
        resetSimulation,
    };
};

export default useChallenge;
