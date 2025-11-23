import { DataSource } from "typeorm";
import { users } from "../entity/user";

export const data_source = new DataSource({
  type: "mysql",
  host: "localhost",
  port: 3306,
  username: "SCP",
  password: "admin",
  database: "smart_city_planner",
  synchronize: true,
  logging: true,
  entities: [users],
});

export const connect_to_database = async () => {
  try {
    // console.log(__dirname + "/entities");
    await data_source.initialize();
    console.log("successfully connected");
  } catch (error) {
    console.error(error);
  }
};
