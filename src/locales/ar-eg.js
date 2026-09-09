/**
 * Arabic (Egypt) Moment locale for HealthPay.
 *
 * Derived from Moment's built-in `ar` locale, which is correct for Egyptian
 * month names (يناير، فبراير …) but renders NUMERALS as Arabic-Indic (١٥).
 * That conflicts with the project's documented numbering decision — Western
 * digits (0-9) for all identifiers, amounts, codes and dates, for claims-data
 * integrity and UHIA reporting compatibility (plan v1 §3.2 item 4).
 *
 * This locale therefore keeps `ar`'s Arabic month/day names and drops the
 * digit conversion by overriding preparse/postformat with identity functions.
 * Week starts Saturday (dow: 6), which matches Egyptian practice.
 */
import moment from "moment";
import "moment/locale/ar";

moment.defineLocale("ar-eg", {
  parentLocale: "ar",
  // Identity preparse/postformat => Western digits, unlike parent `ar`
  preparse: (string) => string,
  postformat: (string) => string,
  week: {
    dow: 6, // Saturday
    doy: 12,
  },
});

// defineLocale switches the global locale as a side effect; restore a neutral
// default so importing this module does not silently change app-wide formatting.
moment.locale("en");

const ARABIC_EGYPT_LOCALE = "ar-eg";

export default ARABIC_EGYPT_LOCALE;
