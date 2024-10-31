import React, { createContext, useState, useContext } from 'react';
import { ChallengeInfo, ChallengeResult, GridState } from '../types/challenge';

interface ChallengeContextType {
    challengeInfo: ChallengeInfo | null;
    setChallengeInfo: React.Dispatch<React.SetStateAction<ChallengeInfo | null>>;
    gridState: GridState | null;
    setGridState: React.Dispatch<React.SetStateAction<GridState | null>>;
    isSimulating: boolean;
    setIsSimulating: React.Dispatch<React.SetStateAction<boolean>>;
    message: string;
    setMessage: React.Dispatch<React.SetStateAction<string>>;
    challengeResult: ChallengeResult;
    setChallengeResult: React.Dispatch<React.SetStateAction<ChallengeResult>>;
}

const ChallengeContext = createContext<ChallengeContextType | undefined>(undefined);

export const ChallengeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [challengeInfo, setChallengeInfo] = useState<ChallengeInfo | null>(null);
    const [gridState, setGridState] = useState<GridState | null>(null);
    const [isSimulating, setIsSimulating] = useState(false);
    const [message, setMessage] = useState('');
    const [challengeResult, setChallengeResult] = useState<ChallengeResult>({
        message: '',
        success: undefined,
        flag: null
    });

    return (
        <ChallengeContext.Provider
            value={{
                challengeInfo,
                setChallengeInfo,
                gridState,
                setGridState,
                isSimulating,
                setIsSimulating,
                message,
                setMessage,
                challengeResult,
                setChallengeResult,
            }}
        >
            {children}
        </ChallengeContext.Provider>
    );
};

export const useChallengeContext = () => {
    const context = useContext(ChallengeContext);
    if (context === undefined) {
        throw new Error('useChallenge must be used within a ChallengeProvider');
    }
    return context;
};
