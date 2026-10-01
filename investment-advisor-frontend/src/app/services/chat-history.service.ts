import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { ApiService } from './api.service';

export interface ChatHistoryItem {
  conversation_id: string;
  title: string;
  created_at: string | null;
  updated_at: string | null;
}

export interface ChatHistoryMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string | null;
}

export interface ChatConversation {
  conversation_id: string;
  title: string;
  created_at: string | null;
  updated_at: string | null;
  messages: ChatHistoryMessage[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatHistoryService {

  constructor(
    private apiService: ApiService
  ) {}

  getConversations(): Observable<{
    conversations: ChatHistoryItem[];
  }> {
    return this.apiService.getData(
      'chat/conversations'
    );
  }

  getConversation(
    conversationId: string
  ): Observable<ChatConversation> {
    return this.apiService.getData(
      `chat/conversations/${conversationId}`
    );
  }
}