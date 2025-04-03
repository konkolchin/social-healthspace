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
