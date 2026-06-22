type MessageHandler = (data: unknown) => void;
type StatusHandler = (status: ConnectionStatus) => void;

export enum ConnectionStatus {
  CONNECTING = "connecting",
  CONNECTED = "connected",
  DISCONNECTED = "disconnected",
  RECONNECTING = "reconnecting",
}

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private accessToken: string | null = null;
  private messageHandlers: Map<string, Set<MessageHandler>> = new Map();
  private statusHandlers: Set<StatusHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectDelay = 1000;
  private status: ConnectionStatus = ConnectionStatus.DISCONNECTED;

  constructor(url: string) {
    this.url = url;
  }

  setAccessToken(token: string | null) {
    this.accessToken = token;
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.setStatus(ConnectionStatus.CONNECTING);
    const wsUrl = `${this.url}?token=${this.accessToken}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.setStatus(ConnectionStatus.CONNECTED);
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { type, payload } = message;
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
          handlers.forEach((handler) => handler(payload));
        }
      } catch {
        console.warn("Failed to parse WebSocket message");
      }
    };

    this.ws.onclose = () => {
      this.setStatus(ConnectionStatus.DISCONNECTED);
      this.reconnect();
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  disconnect() {
    this.reconnectAttempts = this.maxReconnectAttempts;
    this.ws?.close();
    this.ws = null;
    this.setStatus(ConnectionStatus.DISCONNECTED);
  }

  send(type: string, payload: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }));
    }
  }

  on(event: string, handler: MessageHandler) {
    if (!this.messageHandlers.has(event)) {
      this.messageHandlers.set(event, new Set());
    }
    this.messageHandlers.get(event)!.add(handler);
    return () => this.messageHandlers.get(event)?.delete(handler);
  }

  onStatus(handler: StatusHandler) {
    this.statusHandlers.add(handler);
    return () => this.statusHandlers.delete(handler);
  }

  getStatus() {
    return this.status;
  }

  private setStatus(status: ConnectionStatus) {
    this.status = status;
    this.statusHandlers.forEach((handler) => handler(status));
  }

  private reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;

    this.setStatus(ConnectionStatus.RECONNECTING);
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts),
      30000,
    );
    this.reconnectAttempts++;

    setTimeout(() => {
      this.connect();
    }, delay);
  }
}
