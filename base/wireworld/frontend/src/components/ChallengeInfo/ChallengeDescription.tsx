import React from 'react';
import { useChallengeContext } from '../../contexts/ChallengeContext';

const ChallengeDescription: React.FC = () => {
    const { challengeInfo } = useChallengeContext();

    if (!challengeInfo) return null;

    return (
        <div
            dangerouslySetInnerHTML={{ __html: challengeInfo.meta.description }}
            className="max-w-none"
        />
    )
};

export default ChallengeDescription;
