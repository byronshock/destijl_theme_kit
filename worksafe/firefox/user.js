// DeStijl — Firefox preferences. worksafe/firefox/user.js: copied into the profile by install.sh; Firefox
// reads it at every start and it overrides prefs.js. Implements DESTIJL_STYLE.md §0 (declutter), §2 (fonts),
// §3 (curves, motion), §7 Firefox. Remove the file to let Firefox forget it.

// the chrome stylesheet (chrome/userChrome.css, chrome/userContent.css)
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// Firefox draws its own titlebar so the blue tab strip is the key titlebar (§1); COSMIC's header would be the field
user_pref("browser.tabs.inTitlebar", 1);
user_pref("browser.uidensity", 1);                 // compact, as the COSMIC toolkit (§7)
user_pref("browser.compactmode.show", true);
user_pref("widget.gtk.rounded-bottom-corners.enabled", false);   // §3: curves are deprecated
user_pref("widget.gtk.overlay-scrollbars.enabled", false);       // §7: scrollbars always shown
user_pref("ui.prefersReducedMotion", 1);                         // §0: motion is in the user's way
user_pref("layout.css.prefers-color-scheme.content-override", 1);
user_pref("ui.systemUsesDarkTheme", 0);

// §2: Helvetica as Nimbus Sans, Hack for mono. Page content that names its own font keeps it.
user_pref("font.default.x-western", "sans-serif");
user_pref("font.name.sans-serif.x-western", "Nimbus Sans");
user_pref("font.name.serif.x-western", "Nimbus Roman");
user_pref("font.name.monospace.x-western", "Hack");

// Checked against the shipped defaults of Firefox 155.0.1 (deb) on 2026-09-19, by reading
// defaults/preferences/firefox.js and greprefs.js out of omni.ja. Seven prefs this file used to set no
// longer exist in 155 and were removed: extensions.pocket.enabled (Pocket was withdrawn),
// browser.theme.toolbar-theme and its content-theme pair, browser.messaging-system.whatsNewPanel.enabled,
// browser.tabs.firefox-view and its newIcon pair, browser.promo.focus.enabled. A pref for a feature that
// is gone is not harmless -- it is a line that looks like it is doing something.

// §0: the larger half — recommendations, sponsorship, nags, promotions
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.showWeather", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
user_pref("browser.urlbar.suggest.quicksuggest.sponsored", false);
user_pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false);
user_pref("browser.urlbar.suggest.trending", false);
user_pref("browser.urlbar.trending.featureGate", false);
user_pref("browser.urlbar.suggest.recentsearches", false);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.vpn_promo.enabled", false);
user_pref("browser.promo.pin.enabled", false);
user_pref("browser.tabs.hoverPreview.enabled", false);
user_pref("browser.discovery.enabled", false);
user_pref("extensions.getAddons.showPane", false);
user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);

// On by default in Firefox 155, and the same §0 argument as everything above: machine-learning features
// and a promotion pane nobody asked for. Checked against greprefs.js on 2026-09-19.
user_pref("browser.ml.chat.enabled", false);                  // a chatbot in the sidebar
user_pref("browser.tabs.groups.smart.enabled", false);        // machine-suggested tab groups
user_pref("browser.tabs.groups.smart.userEnabled", false);
user_pref("browser.urlbar.suggest.weather", false);
user_pref("browser.preferences.moreFromMozilla", false);      // a promotion pane inside Settings
user_pref("browser.topsites.contile.enabled", false);         // sponsored tiles, at their source
