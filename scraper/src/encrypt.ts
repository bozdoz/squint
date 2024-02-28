import crypto, { CipherGCMTypes } from "node:crypto";
import { Buffer } from "node:buffer";

const ALGO: CipherGCMTypes = "aes-256-gcm";
// random SECRET stored in memory
// aes-256 keys must be 256 bits in length
// https://security.stackexchange.com/questions/266130/generate-aes-256-gcm-key
const SECRET = crypto
  .generateKeySync("aes", {
    length: 256,
  })
  .export();

function getKey(salt: Buffer): Promise<Buffer> {
  // In 2023, OWASP recommended to use 600,000 iterations for PBKDF2-HMAC-SHA256 and 210,000 for PBKDF2-HMAC-SHA512.[6]
  return new Promise((resolve, reject) => {
    crypto.pbkdf2(SECRET, salt, 210_000, 32, "sha512", (err, derivedKey) => {
      if (err) {
        reject(err);
      } else {
        resolve(derivedKey);
      }
    });
  });
}

interface Encrypted {
  iv: string;
  data: string;
  salt: string;
  auth: string;
}

export async function encrypt(plaintext: string): Promise<Encrypted> {
  // The US National Institute of Standards and Technology recommends a salt length of at least 128 bits
  const salt = crypto.randomBytes(128);
  const key = await getKey(salt);

  // iv needs to be 12 bytes
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv(ALGO, key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);

  // all fields can be stored together and used for decryption
  return {
    iv: iv.toString("hex"),
    data: encrypted.toString("hex"),
    salt: salt.toString("hex"),
    auth: cipher.getAuthTag().toString("hex"),
  };
}

// Warning: could throw Error
export async function decrypt(encrypted: Encrypted): Promise<string> {
  const key = await getKey(Buffer.from(encrypted.salt, "hex"));
  const iv = Buffer.from(encrypted.iv, "hex");
  const encryptedText = Buffer.from(encrypted.data, "hex");

  const decipher = crypto.createDecipheriv(ALGO, key, iv);
  decipher.setAuthTag(Buffer.from(encrypted.auth, "hex"));

  const decrypted = Buffer.concat([
    decipher.update(encryptedText),
    decipher.final(),
  ]);

  return decrypted.toString();
}

(async () => {
  const message = await encrypt("MONEY");
  console.log(message);
  console.log(await decrypt(message));
})();
