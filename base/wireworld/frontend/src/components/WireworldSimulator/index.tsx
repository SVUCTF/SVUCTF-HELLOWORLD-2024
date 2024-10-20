import React, { useEffect, useState } from 'react';
import Grid from './Grid';
import ControlPanel from './ControlPanel';
import Tooltip from './Tooltip';
import MessageDisplay from './MessageDisplay';
import { useChallengeContext } from '../../contexts/ChallengeContext';
import useChallenge from '../../hooks/useChallenge';
import { ComponentUnion } from '../../types/wireworld';

const CELL_SIZE = 40;

const WireworldSimulator: React.FC = () => {
    const {
        challengeInfo,
        gridState,
        challengeResult
    } = useChallengeContext();

    const { startSimulation, resetSimulation } = useChallenge('ws://' + window.location.host + '/ws');

    const [tooltipInfo, setTooltipInfo] = useState<{
        x: number;
        y: number;
        component: ComponentUnion | null;
    }>({ x: -1, y: -1, component: null });

    useEffect(() => {
        if (gridState && tooltipInfo.x !== -1 && tooltipInfo.y !== -1) {
            const newComponent = gridState.component_grid[tooltipInfo.y][tooltipInfo.x];
            setTooltipInfo(prev => ({ ...prev, component: newComponent }));
        }
    }, [gridState, tooltipInfo.x, tooltipInfo.y]);

    const handleStartSimulation = () => {
        if (!challengeInfo || !gridState) return;

        const { editable_area } = challengeInfo;
        const editableDesign = gridState.cell_grid
            .slice(editable_area.y, editable_area.y + editable_area.height)
            .map(row => row.slice(editable_area.x, editable_area.x + editable_area.width));

        startSimulation(editableDesign);
    };

    const handleComponentHover = (component: ComponentUnion | null, x: number, y: number) => {
        setTooltipInfo({ x, y, component });
    };

    if (!challengeInfo || !gridState) {
        return <div>Loading...</div>;
    }

    return (
        <div className="flex flex-col h-full">
            <div className="flex-grow overflow-auto flex justify-center">
                <Grid
                    cellSize={CELL_SIZE}
                    onComponentHover={handleComponentHover}
                />
            </div>
            <div className="space-y-2">
                <MessageDisplay challengeResult={challengeResult} />
                <Tooltip component={tooltipInfo.component} />
                <ControlPanel
                    onStart={handleStartSimulation}
                    onReset={resetSimulation}
                    currentStep={gridState.step}
                    maxSteps={challengeInfo.grid.max_steps}
                />
            </div>
        </div>
    );
};

export default WireworldSimulator;
