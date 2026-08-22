import React from "react";
import { useSelector } from "react-redux";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import MomentUtils from "@date-io/moment";
import moment from "moment";
import "./locales/ar-eg";

/**
 * Supplies the Moment locale to the date pickers based on the authenticated
 * user's language.
 *
 * Without this, `MuiPickersUtilsProvider utils={MomentUtils}` runs on Moment's
 * default `en` locale, so the birth-date calendar rendered entirely in English
 * ("Sat, Aug 22", "August 2026", OK/CANCEL/CLEAR) inside the Arabic RTL
 * enrolment form.
 *
 * Mapping: any `ar*` user language -> `ar-eg` (see src/locales/ar-eg.js:
 * Arabic month names, Western digits, Saturday week start). Anything else keeps
 * the browser/user language as-is.
 */
const LocalizedPickersProvider = ({ children }) => {
  const userLanguage = useSelector(
    (state) => state?.core?.user?.i_user?.language ?? null
  );
  const lang = typeof userLanguage === "string" ? userLanguage : "";
  const locale = lang.toLowerCase().startsWith("ar") ? "ar-eg" : lang || "en";

  React.useEffect(() => {
    moment.locale(locale);
  }, [locale]);

  return (
    <MuiPickersUtilsProvider utils={MomentUtils} locale={locale}>
      {children}
    </MuiPickersUtilsProvider>
  );
};

export default LocalizedPickersProvider;
