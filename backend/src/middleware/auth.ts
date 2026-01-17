import { Request, Response, NextFunction } from "express";
import { verification } from "../utils/jwtUtils";

export function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const auth = req.headers.authorization;

  if (!auth) {
    return res.status(401).json({ message: "No token provided" });
  }

  const token = auth.split(" ")[1];

  try {
    const decoded = verification(token);
    req.body.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ message: "Invalid token" });
  }
}
