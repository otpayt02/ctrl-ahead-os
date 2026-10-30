/* shared.js — Ctrl-Ahead Argon video: minimal GSAP helpers.
 * Rules honoured: paused timelines registered on window.__timelines by the
 * caller via makeSceneTimeline; fromTo preferred; transforms/opacity/color
 * only; no Date.now()/Math.random()/network — everything is a pure function
 * of timeline time. */
(function () {
  function makeSceneTimeline(compositionId, duration) {
    const tl = gsap.timeline({ paused: true });
    const hold = { p: 0 };
    tl.to(hold, { p: 1, duration: duration, ease: "none" }, 0);
    window.__timelines = window.__timelines || {};
    window.__timelines[compositionId] = tl;
    return tl;
  }

  /* Pin a card: scale 0.8 -> 1, y settle, back.out overshoot. */
  function pinCard(el, tl, position, dur) {
    tl.fromTo(
      el,
      { scale: 0.8, y: 48, opacity: 0 },
      { scale: 1, y: 0, opacity: 1, duration: dur || 0.45, ease: "back.out(1.8)" },
      position
    );
    return tl;
  }

  /* Stamp a chip: hard scale-in with a tiny rotation settle (evidence stamp). */
  function stampIn(el, tl, position) {
    tl.fromTo(
      el,
      { scale: 1.6, opacity: 0, rotation: -6 },
      { scale: 1, opacity: 1, rotation: 0, duration: 0.28, ease: "power4.out" },
      position
    );
    return tl;
  }

  /* Camera settle: quick dolly from `from` to `to` (scene-open settle only,
   * never a slow zoom). */
  function cameraPush(rootEl, fromScale, toScale, duration, tl, position) {
    tl.fromTo(
      rootEl,
      { scale: fromScale, transformOrigin: "50% 50%" },
      { scale: toScale, duration: duration, ease: "power1.inOut" },
      position
    );
    return tl;
  }

  /* Pulse a badge/button once: 1 -> 1.15 -> 1. */
  function pulseBadge(badgeEl, tl, position) {
    tl.fromTo(badgeEl, { scale: 1 }, { scale: 1.15, duration: 0.2, ease: "power2.out" }, position);
    tl.to(badgeEl, { scale: 1, duration: 0.26, ease: "power2.inOut", immediateRender: false }, position + 0.2);
    return tl;
  }

  /* Count-up number: deterministic object tween, formatted on update. */
  function countUp(el, from, to, duration, tl, position, fmt) {
    const state = { v: from };
    const format = fmt || function (v) { return Math.round(v).toLocaleString("en-US"); };
    tl.to(state, {
      v: to, duration: duration, ease: "power2.out",
      onUpdate: function () { el.textContent = format(state.v); },
    }, position);
    el.textContent = format(from);
    return tl;
  }

  /* Caption driver: phrases = [{el, start, end, words:[[el, start, end],...]}]
   * Phrase fades in at start, out at end (de-overlapped by the caller).
   * Each word: dim-white before, GOLD while spoken, full white after. */
  function driveCaptions(tl, phrases) {
    phrases.forEach(function (p) {
      tl.fromTo(p.el, { opacity: 0 }, { opacity: 1, duration: 0.07, ease: "none" }, p.start);
      tl.fromTo(p.el, { opacity: 1 }, { opacity: 0, duration: 0.07, ease: "none", immediateRender: false }, Math.max(p.end - 0.07, p.start + 0.07));
      p.words.forEach(function (w) {
        tl.fromTo(w[0], { color: "rgba(255,255,255,0.42)" }, { color: "#ffd166", duration: 0.05, ease: "none" }, w[1]);
        tl.fromTo(w[0], { color: "#ffd166" }, { color: "#ffffff", duration: 0.05, ease: "none", immediateRender: false }, w[2]);
      });
    });
    return tl;
  }

  window.makeSceneTimeline = makeSceneTimeline;
  window.pinCard = pinCard;
  window.stampIn = stampIn;
  window.cameraPush = cameraPush;
  window.pulseBadge = pulseBadge;
  window.countUp = countUp;
  window.driveCaptions = driveCaptions;
})();
