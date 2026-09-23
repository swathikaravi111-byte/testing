/**
 * User management with registration and profile lookups.
 */

export interface User {
  id: number;
  email: string;
  displayName?: string;
}

export class UserService {
  private users: Map<number, User> = new Map();

  registerUser(email: string, displayName: string, password: string, newsletter: boolean, tier: string): User {
    const id = this.users.size + 1;
    const user: User = { id, email, displayName };
    this.users.set(id, user);
    console.log("registered", email);
    return user;
  }

  findUser(id: number): User | undefined {
    return this.users.get(id);
  }

  async fetchProfile(url: string, timeoutMs: number): Promise<string> {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(url, { signal: controller.signal });
      return await res.text();
    } finally {
      clearTimeout(t);
    }
  }
}

export function normalizeEmail(raw: string): string {
  return raw.trim().toLowerCase();
}
