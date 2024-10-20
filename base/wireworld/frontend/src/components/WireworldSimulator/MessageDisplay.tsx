import React from 'react';
import { ChallengeResult } from '../../types/challenge';

interface MessageDisplayProps {
    challengeResult: ChallengeResult;
}

const MessageDisplay: React.FC<MessageDisplayProps> = ({ challengeResult }) => {
    const { message, success, flag } = challengeResult;

    if (!message) return null;

    const bgColor = success ? 'bg-nord14' : 'bg-nord11';

    return (
        <div className={`p-4 ${bgColor} text-nord6 rounded mt-2 mb-2`}>
            <p className="font-semibold">{message}</p>
            {success && flag && (
                <p className="mt-2">Flag: {flag}</p>
            )}
        </div>
    );
};

export default MessageDisplay;
