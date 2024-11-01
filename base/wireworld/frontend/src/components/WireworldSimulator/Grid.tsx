import React from 'react';
import { useChallengeContext } from '../../contexts/ChallengeContext';
import { ComponentUnion, CellUnion } from '../../types/wireworld';
import { CELL_COLORS } from '../../constants/cellColors';
import ComponentIcon from './ComponentIcon';
import { COMPONENT_COLORS } from '../../constants/componentColors';

interface GridProps {
    cellSize: number;
    onComponentHover: (component: ComponentUnion | null, x: number, y: number) => void;
}

const Grid: React.FC<GridProps> = ({ cellSize, onComponentHover }) => {
    const { challengeInfo, gridState, isSimulating, setGridState } = useChallengeContext();

    if (!challengeInfo || !gridState) return null;

    const { grid, editable_area } = challengeInfo;

    const handleCellClick = (x: number, y: number) => {
        if (isSimulating) return;

        if (x < editable_area.x || x >= editable_area.x + editable_area.width ||
            y < editable_area.y || y >= editable_area.y + editable_area.height) {
            return;
        }

        const currentCellType = gridState.cell_grid[y][x].type;
        const cellOrder: CellUnion['type'][] = ['EmptyCell', 'Conductor', 'ElectronHead', 'ElectronTail'];
        const currentIndex = cellOrder.indexOf(currentCellType);
        const nextIndex = (currentIndex + 1) % cellOrder.length;
        const nextCellType = cellOrder[nextIndex];

        const newGridState = {
            ...gridState,
            cell_grid: gridState.cell_grid.map((row, rowIndex) =>
                rowIndex === y
                    ? row.map((cell, colIndex) =>
                        colIndex === x ? { type: nextCellType } : cell
                    )
                    : row
            ),
        };

        setGridState(newGridState);
    };

    const isEditable = (x: number, y: number) => {
        return x >= editable_area.x && x < editable_area.x + editable_area.width &&
            y >= editable_area.y && y < editable_area.y + editable_area.height;
    };


    const renderComponent = (component: ComponentUnion | null) => {
        if (!component) return null;

        const iconSize = cellSize * 0.7;
        let className = COMPONENT_COLORS[component.type];

        return <ComponentIcon component={component} size={iconSize} className={className} />;
    };

    return (
        <div className="relative">
            <div
                className="grid gap-px bg-nord3"
                style={{
                    gridTemplateColumns: `repeat(${grid.width}, ${cellSize}px)`,
                    gridTemplateRows: `repeat(${grid.height}, ${cellSize}px)`,
                    width: `${grid.width * (cellSize + 1) - 1}px`,
                    height: `${grid.height * (cellSize + 1) - 1}px`,
                }}
            >
                {gridState.cell_grid.map((row, y) =>
                    row.map((cell, x) => {
                        const editable = isEditable(x, y);
                        const component = gridState.component_grid[y][x];
                        return (
                            <div
                                key={`${x}-${y}`}
                                className={`
                                    ${CELL_COLORS[cell.type]}
                                    ${editable ? 'cursor-pointer' : 'cursor-default'}
                                    relative flex items-center justify-center
                                `}
                                style={{ width: `${cellSize}px`, height: `${cellSize}px` }}
                                onClick={() => handleCellClick(x, y)}
                                onMouseEnter={() => onComponentHover(component, x, y)}
                                onMouseLeave={() => onComponentHover(null, -1, -1)}
                            >
                                {renderComponent(component)}
                            </div>
                        );
                    })
                )}
            </div>
            <div
                className="absolute border-2 border-nord7 pointer-events-none"
                style={{
                    left: `${editable_area.x * (cellSize + 1)}px`,
                    top: `${editable_area.y * (cellSize + 1)}px`,
                    width: `${editable_area.width * (cellSize + 1) - 1}px`,
                    height: `${editable_area.height * (cellSize + 1) - 1}px`,
                }}
            />
        </div>
    );
};

export default Grid;
