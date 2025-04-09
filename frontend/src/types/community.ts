export interface Community {
  id: number;
  name: string;
  slug: string;
  description: string;
  is_private: boolean;
  created_at: string;
  created_by_id: number;
  members_count: number;
  is_member: boolean;
  is_admin: boolean;
}

export interface CommunityCreate {
  name: string;
  description?: string;
  is_private: boolean;
}

export interface CommunityUpdate {
  name?: string;
  description?: string;
  is_private?: boolean;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  author_name?: string;
  created_at: string;
  updated_at: string;
  author_id: number;
  community_id?: number;
  community?: CommunityMinimal;
  likes_count: number;
  comments_count: number;
  is_announcement?: boolean;
  is_liked?: boolean;
  comments?: any[];
}

export interface CommunityMinimal {
  id: number;
  name: string;
  slug: string;
  description: string;
}
