import { defineConfig } from "./src/config";

export default defineConfig({
  mount: {
    manual: true,
    databases: [
      {
        // database_id: "eb897916879243289a3612c1b793c43f",
        database_id: "1987522eeb2f8116865ec0c41fe31412",
        target_folder: "posts",
      },
    ],
  },
});
