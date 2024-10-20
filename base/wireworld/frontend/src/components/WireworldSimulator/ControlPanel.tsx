import React from 'react';
import { Button } from '../ui/Button';
import { useChallengeContext } from '../../contexts/ChallengeContext';

interface ControlPanelProps {
    onStart: () => void;
    onReset: () => void;
    currentStep: number;
    maxSteps: number;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
    onStart,
    onReset,
    currentStep,
    maxSteps,
}) => {
    const { isSimulating } = useChallengeContext();
    return (
        <div className="flex justify-between items-center bg-nord2 p-4 rounded">
            <div>
                <Button onClick={onStart} className="mr-2" disabled={isSimulating}>
                    Start
                </Button>
                <Button onClick={onReset} variant="danger" disabled={isSimulating}>
                    Reset
                </Button>
            </div>
            <div className="text-nord6">
                Step: <span className="font-semibold">{currentStep} / {maxSteps}</span>
            </div>
        </div>
    );
};

export default ControlPanel;
