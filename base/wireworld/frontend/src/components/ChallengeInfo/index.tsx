import React from 'react';
import { Card } from '../ui/Card';
import ChallengeDescription from './ChallengeDescription';
import CellTypeInfo from './CellTypeInfo';
import ComponentTypeInfo from './ComponentTypeInfo';
import HelpInfo from './HelpInfo';

const ChallengeInfo: React.FC = () => {
    return (
        <>
            <Card title="挑战描述">
                <ChallengeDescription />
            </Card>
            <Card title="帮助信息" className="mt-6">
                <HelpInfo />
            </Card>
            <Card title="细胞类型" className="mt-6">
                <CellTypeInfo />
            </Card>
            <Card title="组件类型" className="mt-6">
                <ComponentTypeInfo />
            </Card>
        </>
    );
};

export default ChallengeInfo;
