import jwt from "jsonwebtoken";
import { TokenPayload } from "../model/tokenPayload";

/*export function generateKey():string{
    return crypto.randomBytes(64).toString('hex')
}*/

const key = "jbjasdbsjdbsj";

export function payload(username: string) {
  return { username };
}

export function generateJWT(payload: object): string {
  return jwt.sign(payload, key, { expiresIn: "1h" });
}

export function verification(token: string): TokenPayload {
  try {
    return jwt.verify(token, key) as TokenPayload;
  } catch (error) {
    throw error;
  }
}
