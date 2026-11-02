// Buzz 1.0 plugin (block/buzz-app, API v1): prebuilt module, no build step and
// no dependencies. It reads the lifecycle markers that project-buzz writes and
// never signs, sends or stores anything.
export const inject = ["react", "conversation"];

// MARKER_RE from plugins/buzz-comms/scripts/project-buzz, anchored to the start
// of the post: the helper writes the marker as the first line, and anchoring
// keeps a post that merely quotes a marker from getting a badge.
const MARKER_RE =
  /^\s*\[AGENT-(?:ACTIVITY:(started|progress|blocked|correction)|RESULT):([a-z0-9][a-z0-9._-]{0,31}):([A-Za-z0-9][A-Za-z0-9._-]{0,63})\]/;
const CLOSING_PHASES = ["result", "blocked", "correction"];
const LABELS = {
  started: "Start",
  progress: "Zwischenstand",
  result: "Ergebnis",
  blocked: "Blockiert",
  correction: "Korrektur",
};
// Host tokens from plain :root blocks only: variables that exist solely in a
// Tailwind `@theme inline` block (such as --text-color-danger) never reach the
// page, and the color silently falls back to the inherited text color.
const COLORS = {
  result: "var(--text-success)",
  blocked: "var(--text-danger)",
  correction: "var(--text-warning)",
};
const EXCERPT_LENGTH = 120;

/** Parse a lifecycle post; null when the post does not open with a marker. */
export function parseLifecycle(content) {
  const text = String(content ?? "");
  const match = MARKER_RE.exec(text);
  if (!match) return null;
  return {
    phase: match[1] ?? "result",
    agent: match[2],
    updateId: match[3],
    // Same as text_after_marker in project-buzz: drop the ": #" definition tail.
    text: text
      .slice(match[0].length)
      .replace(/^:[ \t]*#/, "")
      .trim(),
  };
}

/**
 * Lifecycle state of one thread, by the rule `project-buzz open` uses: a
 * thread is closed once it holds a result, blocker or correction, and open
 * while it has a start and none of those.
 */
export function threadState(messages) {
  const entries = [];
  for (const message of messages) {
    const parsed = parseLifecycle(message.sourceContent ?? message.content);
    if (parsed)
      entries.push({ ...parsed, id: message.id, createdAt: message.createdAt });
  }
  entries.sort((a, b) => a.createdAt - b.createdAt);
  const closing = entries
    .filter((entry) => CLOSING_PHASES.includes(entry.phase))
    .at(-1);
  const started = entries.some((entry) => entry.phase === "started");
  return {
    entries,
    closing,
    state: closing ? "closed" : started ? "open" : "none",
  };
}

function excerpt(text) {
  const line = (text.split("\n").find((row) => row.trim()) ?? "")
    .replace(/\*\*|`/g, "")
    .trim();
  return line.length > EXCERPT_LENGTH
    ? `${line.slice(0, EXCERPT_LENGTH - 1)}…`
    : line;
}

export function apply(ctx) {
  const React = ctx.react;
  const h = React.createElement;
  const format = ctx.conversation.format;
  const lifecycleOf = (message) =>
    parseLifecycle(message.sourceContent ?? message.content);
  // Host buttons otherwise keep the browser's control font size.
  const buttonStyle = { font: "inherit" };

  // Tabler "list-check", the icon set the host menu uses, at its menu size.
  function ListCheckIcon() {
    return h(
      "svg",
      {
        "aria-hidden": true,
        width: "1rem",
        height: "1rem",
        viewBox: "0 0 24 24",
        fill: "none",
        stroke: "currentColor",
        strokeWidth: 2,
        strokeLinecap: "round",
        strokeLinejoin: "round",
      },
      [
        "M3.5 5.5l1.5 1.5l2.5 -2.5",
        "M3.5 11.5l1.5 1.5l2.5 -2.5",
        "M3.5 17.5l1.5 1.5l2.5 -2.5",
        "M11 6l9 0",
        "M11 12l9 0",
        "M11 18l9 0",
      ].map((d) => h("path", { key: d, d })),
    );
  }

  function PhaseLabel({ phase }) {
    return h(
      "span",
      {
        style: {
          color: COLORS[phase] ?? "var(--text-subtle)",
          fontSize: "var(--type-size-12)",
          lineHeight: 1.3333,
          fontWeight: 600,
          whiteSpace: "nowrap",
        },
      },
      LABELS[phase],
    );
  }

  function PhaseMark({ message }) {
    const parsed = lifecycleOf(message);
    if (!parsed) return null;
    return h(
      "span",
      { title: `${LABELS[parsed.phase]} von ${parsed.agent}: ${parsed.updateId}` },
      h(PhaseLabel, { phase: parsed.phase }),
    );
  }

  function summary(state) {
    if (state.state === "closed") {
      const { phase, agent, createdAt } = state.closing;
      return `Abgeschlossen: ${LABELS[phase]} von ${agent}, ${format.itemTimestamp(createdAt, { withTime: true })}.`;
    }
    if (state.state === "open")
      return "Offen: noch kein Ergebnis, kein Blocker und keine Korrektur.";
    return "Dieser Thread enthält keinen Lifecycle-Start.";
  }

  function ThreadPanel({ view }) {
    const snapshot = React.useSyncExternalStore(
      view.subscribe,
      view.snapshot,
      view.snapshot,
    );
    if (snapshot.status === "error")
      return h(
        React.Fragment,
        null,
        h(
          "p",
          { role: "alert" },
          `Thread nicht lesbar: ${snapshot.error ?? "unbekannter Fehler"}`,
        ),
        h(
          "button",
          {
            type: "button",
            style: buttonStyle,
            onClick: () => void view.refresh(),
          },
          "Erneut laden",
        ),
      );
    if (snapshot.status !== "ready" || !snapshot.root)
      return h("p", { role: "status" }, "Thread wird geladen …");
    const state = threadState([snapshot.root, ...snapshot.replies]);
    return h(
      React.Fragment,
      null,
      h("p", { role: "status", style: { margin: 0 } }, summary(state)),
      snapshot.canLoadMore &&
        h(
          "p",
          { style: { margin: 0, color: "var(--text-subtle)" } },
          "Ältere Antworten sind nicht geladen, der Stand kann deshalb unvollständig sein. ",
          h(
            "button",
            {
              type: "button",
              style: buttonStyle,
              onClick: () => void view.loadMore(),
            },
            "Ältere Antworten laden",
          ),
        ),
      state.entries.length > 0 &&
        h(
          "ol",
          {
            style: {
              margin: 0,
              paddingInlineStart: "var(--space-4)",
              display: "grid",
              gap: "var(--space-1)",
            },
          },
          state.entries.map((entry) =>
            h(
              "li",
              { key: entry.id },
              h(PhaseLabel, { phase: entry.phase }),
              ` ${entry.agent}, ${format.itemTimestamp(entry.createdAt, { withTime: true })}: ${excerpt(entry.text)}`,
            ),
          ),
        ),
    );
  }

  function ThreadStatus({ message, session, close }) {
    const rootId = message.threadRootId ?? message.id;
    const [view, setView] = React.useState();
    const [failure, setFailure] = React.useState();
    const panel = React.useRef(null);
    // One reader, opened on request and disposed with the panel: thread views
    // are capped app-wide, so the marker never opens one.
    React.useEffect(() => {
      try {
        const owned = session.thread(message.channelId, rootId);
        setView(owned);
        void owned.refresh();
        return () => owned.dispose();
      } catch (error) {
        setFailure(String(error?.message ?? error));
      }
    }, [session, message.channelId, rootId]);
    React.useEffect(() => panel.current?.focus(), []);
    return h(
      "section",
      {
        ref: panel,
        tabIndex: -1,
        "aria-label": "Lifecycle-Stand des Threads",
        onKeyDown: (event) => {
          if (event.key === "Escape") {
            event.stopPropagation();
            close();
          }
        },
        style: {
          display: "grid",
          gap: "var(--space-2)",
          marginBlockStart: "var(--space-2)",
          padding: "var(--space-3)",
          border: "1px solid var(--border-standard)",
          borderRadius: "var(--radius-panel)",
          background: "var(--surface-panel)",
          fontSize: "var(--type-size-14)",
          lineHeight: 1.4286,
        },
      },
      failure
        ? h("p", { role: "alert" }, `Thread nicht lesbar: ${failure}`)
        : view
          ? h(ThreadPanel, { view })
          : h("p", { role: "status" }, "Thread wird geladen …"),
      h(
        "div",
        null,
        h(
          "button",
          { type: "button", style: buttonStyle, onClick: close },
          "Schließen",
        ),
      ),
    );
  }

  ctx.conversation.registerMessageAction({
    id: "lifecycle-status",
    title: "Lifecycle-Stand anzeigen",
    icon: ListCheckIcon,
    matches: (message) => lifecycleOf(message) !== null,
    component: ThreadStatus,
    marker: PhaseMark,
  });
}
