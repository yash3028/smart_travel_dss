import app from "./index";
import { connect_to_database } from "./config/database";

app.listen(3001, async () => {
  console.log(`listening on port 3001`);
  await connect_to_database();
});
