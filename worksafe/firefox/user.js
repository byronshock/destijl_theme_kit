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
user_pref("browser.theme.toolbar-theme", 1);                     // light (§7: the system's polarity is BLACK on WHITE)
user_pref("browser.theme.content-theme", 1);
user_pref("layout.css.prefers-color-scheme.content-override", 1);
user_pref("ui.systemUsesDarkTheme", 0);

// §2: Helvetica as Nimbus Sans, Hack for mono. Page content that names its own font keeps it.
user_pref("font.default.x-western", "sans-serif");
user_pref("font.name.sans-serif.x-western", "Nimbus Sans");
user_pref("font.name.serif.x-western", "Nimbus Roman");
user_pref("font.name.monospace.x-western", "Hack");

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
user_pref("extensions.pocket.enabled", false);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.messaging-system.whatsNewPanel.enabled", false);
user_pref("browser.vpn_promo.enabled", false);
user_pref("browser.promo.focus.enabled", false);
user_pref("browser.promo.pin.enabled", false);
user_pref("browser.tabs.hoverPreview.enabled", false);
user_pref("browser.tabs.firefox-view", false);
user_pref("browser.tabs.firefox-view-newIcon", false);
user_pref("browser.discovery.enabled", false);
user_pref("extensions.getAddons.showPane", false);
user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);
