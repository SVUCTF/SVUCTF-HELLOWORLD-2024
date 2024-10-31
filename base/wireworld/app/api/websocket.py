from typing import Annotated
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import TypeAdapter, ValidationError
from pydantic import Field

from app.services.challenge import ChallengeService
from app.services.connection_manager import ConnectionManager
from app.schemas.challenge import (
    ResetMessage,
    WebSocketMessageUnion,
    SimulateMessage,
    GetInfoMessage,
    WorldUpdateMessage,
    SimulationResultMessage,
    ChallengeInfoMessage,
    ErrorMessage,
)

manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    type_adapter: TypeAdapter[WebSocketMessageUnion] = TypeAdapter(
        Annotated[WebSocketMessageUnion, Field(discriminator="type")]
    )
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = type_adapter.validate_json(data)

                if isinstance(message, SimulateMessage):
                    await handle_simulate(message.design, websocket)
                elif isinstance(message, GetInfoMessage):
                    await handle_get_info(websocket)
                elif isinstance(message, ResetMessage):
                    await handle_reset(websocket)
                else:
                    await send_error("Unknown message type", websocket)

            except ValidationError as e:
                await send_error(f"Invalid message format: {str(e)}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def handle_simulate(design, websocket: WebSocket):
    async for grid_state in ChallengeService.run_simulation(design):
        await manager.send_personal_message(
            WorldUpdateMessage(grid_state=grid_state).model_dump_json(),
            websocket,
        )

    result = ChallengeService.get_simulation_result()
    await manager.send_personal_message(
        SimulationResultMessage(
            success=result.success,
            final_state=result.final_state,
            flag=result.flag,
        ).model_dump_json(),
        websocket,
    )


async def handle_get_info(websocket: WebSocket):
    info = ChallengeService.get_challenge_info()
    await manager.send_personal_message(
        ChallengeInfoMessage(
            meta=info.meta,
            grid=info.grid,
            initial_state=info.initial_state,
            editable_area=info.editable_area,
        ).model_dump_json(),
        websocket,
    )


async def handle_reset(websocket: WebSocket):
    ChallengeService.reset()
    await handle_get_info(websocket)


async def send_error(message: str, websocket: WebSocket):
    await manager.send_personal_message(
        ErrorMessage(type="error", message=message).model_dump_json(), websocket
    )
