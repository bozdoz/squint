import { firefox, devices } from "playwright";
import { signin } from "./accounts/BMO/signin";

(async () => {
  // Setup
  const browser = await firefox.launch({ headless: false, devtools: true });
  const context = await browser.newContext(devices["Desktop Firefox"]);
  const page = await context.newPage();

  // don't fetch any images
  await context.route("**/*.{webp,gif,svg,png,jpg,jpeg}", (route) =>
    route.abort()
  );

  const login = "1111222233334444";
  const password = "asdfasdfasdfasdfasdfasdf";

  await signin({ page, login, password });

  process.addListener("SIGINT", async () => {
    // Teardown
    await context.close();
    await browser.close();
  });
})();
