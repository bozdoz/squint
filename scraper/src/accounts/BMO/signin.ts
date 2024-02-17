import { Page } from "playwright";

interface PageAuth {
  page: Page;
  login: string;
  password: string;
}

const LOGIN_PAGE = "https://www.bmo.com/en-ca/main/personal/";
const ACCOUNTS_PAGE = "https://www1.bmo.com/banking/digital/accounts";

export const signin = async ({ page, login, password }: PageAuth) => {
  await page.goto(LOGIN_PAGE);
  await page
    .getByRole("button", { name: "Toggle sign in menu navigation" })
    .click();
  await page.getByRole("link", { name: "Access online banking" }).click();
  await page.getByLabel("Card number").click();
  await page.getByLabel("Card number").fill(login);
  await page.getByLabel("Password", { exact: true }).click();
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Sign in" }).click();

  // need to await details page or verification page
  let atAccountPage = false;
  let accountPage = page.waitForURL(ACCOUNTS_PAGE).then(() => {
    atAccountPage = true;
  });
  let needsVerification = false;
  let verification = page
    .getByRole("heading", { name: "Security Verification" })
    .isVisible()
    .then(() => {
      needsVerification = true;
    });

  await Promise.race([accountPage, verification]);

  if (atAccountPage) {
    // hooray!
  } else if (needsVerification) {
    // TODO: send choices to logged in user?
    await page.getByRole("button", { name: "NEXT" }).click();

    // we always want email
    await page.getByRole("radio", { name: /^Email.*/ }).click();
    // confirm
    await page.getByRole("checkbox").setChecked(true);
    await page.getByRole("button", { name: "SEND CODE" }).click();

    // TODO: send input back to logged in user, who then puts in code

    // ALT: send a new code:
    // name:"Send a new code"
    // role:"link"

    // TODO: code
    await page
      .getByRole("textbox", { name: "Enter verification code" })
      .fill("123456");
    await page.getByRole("button", { name: "CONFIRM" }).click();

    // trust this device
    // name:"Trust this Device"
    // role:"checkbox"

    //   name:"CONTINUE"
    // role:"button"
  }
};
