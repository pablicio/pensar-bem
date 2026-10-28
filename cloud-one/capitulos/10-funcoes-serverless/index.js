const { Storage } = require("@google-cloud/storage");
const sharp = require("sharp");
const storage = new Storage();

exports.miniatura = async (evento) => {
  const { bucket, name } = evento.data;
  if (!name.startsWith("barracas/")) return;

  const [original] = await storage.bucket(bucket)
    .file(name).download();
  const mini = await sharp(original)
    .resize(320, 320, { fit: "cover" })
    .webp({ quality: 75 }).toBuffer();

  await storage.bucket("arraia-miniaturas")
    .file(name.replace(/\.\w+$/, ".webp")).save(mini);
};
