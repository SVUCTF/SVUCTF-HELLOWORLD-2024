import React from 'react';
import { useChallengeContext } from '../../contexts/ChallengeContext';
import { CELL_COLORS } from '../../constants/cellColors';

const CellTypeInfo: React.FC = () => {
    const { challengeInfo } = useChallengeContext();

    if (!challengeInfo) return null;

    const { cell_descriptions } = challengeInfo.meta;

    return (
        <div>
            {Object.entries(cell_descriptions).map(([cellType, description]) => (
                <div key={cellType} className="flex items-center mb-4">
                    <div className="w-6 h-6 flex-shrink-0 mr-4">
                        <div
                            className={`w-full h-full ${CELL_COLORS[cellType as keyof typeof CELL_COLORS]} rounded`}
                        ></div>
                    </div>
                    <div>
                        <h4 className="font-semibold capitalize">{cellType}</h4>
                        <p className="text-sm">{description}</p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default CellTypeInfo;
