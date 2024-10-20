import React from 'react';
import { useChallengeContext } from '../../contexts/ChallengeContext';
import { COMPONENT_COLORS } from '../../constants/componentColors';
import ComponentIcon from '../WireworldSimulator/ComponentIcon';
import { ComponentUnion } from '../../types/wireworld';

const ComponentTypeInfo: React.FC = () => {
    const { challengeInfo } = useChallengeContext();

    if (!challengeInfo) return null;

    const { component_descriptions } = challengeInfo.meta;

    return (
        <div>
            {Object.entries(component_descriptions).map(([componentType, description]) => (
                <div key={componentType} className="flex items-center mb-4">
                    <div className="w-6 h-6 flex-shrink-0 mr-4 flex items-center justify-center">
                        <ComponentIcon
                            component={{ type: componentType } as ComponentUnion}
                            size={32}
                            className={COMPONENT_COLORS[componentType as keyof typeof COMPONENT_COLORS]}
                        />
                    </div>
                    <div>
                        <h4 className="font-semibold capitalize">{componentType}</h4>
                        <p className="text-sm">{description}</p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ComponentTypeInfo;
