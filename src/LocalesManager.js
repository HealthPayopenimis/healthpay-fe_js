import { fileNamesByLang } from "./locales";

class LocalesManager {
  getPublicDefaultLanguage() {
    // HealthPay's Egypt portal is Arabic-first before authentication. The
    // public-page language cookie still takes precedence in fe-core, and an
    // authenticated user's stored language remains authoritative.
    return "ar";
  }

  getLocale(lang) {
    // messages in requested language are injected as the default 'en' locale
    return "en";
  }

  getFileNameByLang(lang) {
    return fileNamesByLang[lang];
  }
}

export default LocalesManager;
