import { useEffect, useRef, useCallback } from 'react';

type WebSocketMessage = string | ArrayBufferLike | Blob | ArrayBufferView;


const useWebSocket = (url: string, onMessage: (data: any) => void) => {
    const socket = useRef<WebSocket | null>(null);

    useEffect(() => {
        socket.current = new WebSocket(url);

        socket.current.onopen = () => {
            console.log('WebSocket connected');
            sendMessage(JSON.stringify({ type: 'get_info' }))
        };

        socket.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessage(data);
        };

        return () => {
            if (socket.current) {
                socket.current.close();
            }
        };
    }, [url, onMessage]);

    const sendMessage = useCallback((message: WebSocketMessage) => {
        if (socket.current && socket.current.readyState === WebSocket.OPEN) {
            socket.current.send(message);
        } else {
            console.error('WebSocket is not connected');
        }
    }, []);

    return { sendMessage };
};

export default useWebSocket;
