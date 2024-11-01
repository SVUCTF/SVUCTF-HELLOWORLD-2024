import React from 'react';
import WireworldSimulator from './components/WireworldSimulator';
import ChallengeInfo from './components/ChallengeInfo';
import { ChallengeProvider, useChallengeContext } from './contexts/ChallengeContext';

const AppContent: React.FC = () => {
    const { challengeInfo } = useChallengeContext();

    return (
        <div className="App flex flex-col h-screen bg-nord0 text-nord6">
            <header className="bg-nord1 text-nord6 p-4">
                <h1 className="text-2xl font-bold">
                    {challengeInfo?.meta.name || 'Loading...'}
                </h1>
            </header>
            <div className="flex flex-1 overflow-hidden">
                <div className="w-1/3 p-4 overflow-y-auto bg-nord1">
                    <ChallengeInfo />
                </div>
                <div className="flex-1 p-4 flex flex-col bg-nord0 overflow-hidden">
                    <WireworldSimulator />
                </div>
            </div>
        </div>
    );
};

const App: React.FC = () => {
    return (
        <ChallengeProvider>
            <AppContent />
        </ChallengeProvider>
    );
};

export default App;
