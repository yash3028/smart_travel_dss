import { Request, Response, NextFunction, Router } from "express";
import { login, signup } from "../services/userService";

const router: Router = Router();
router.post(
  "/save-user",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      res.status(201).send(await signup(req.body));
    } catch (error) {
      next(error);
    }
  }
);

router.post(
  "/login",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const login_response = await login(req.body);
      if (login_response?.success) {
        res
          .status(200)
          .json({ message: "successful", token: login_response.token });
      } else {
        res.status(401).json({ message: "unauthorized" });
      }
    } catch (error) {
      next(error);
    }
  }
);

export = router;
