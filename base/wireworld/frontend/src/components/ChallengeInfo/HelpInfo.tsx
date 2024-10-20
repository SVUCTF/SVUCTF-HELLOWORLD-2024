import React from 'react';

const HelpInfo: React.FC = () => {
    return (
        <div className="space-y-4">
            <p>
                欢迎来到 Wireworld 挑战，你的目标是设计一个满足特定条件的电路。
            </p>
            <ul className="list-disc pl-5 space-y-2">
                <li>在右侧网格的高亮区域内放置细胞</li>
                <li>左键点击可在不同细胞类型间切换</li>
                <li>「Start」开始模拟，「Reset」重置世界</li>
                <li>在规定步数内完成挑战条件即可获得 Flag</li>
            </ul>
        </div>
    );
};

export default HelpInfo;
