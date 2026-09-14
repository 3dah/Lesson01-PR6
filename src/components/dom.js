export function el(tag, className, attrs = {}) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'text') node.textContent = v;
    else if (k === 'html') node.innerHTML = v;
    else node.setAttribute(k, v);
  }
  return node;
}

export function sceneShell(chapter, { visual, actions } = {}) {
  const root = el('section', 'scene');
  root.dataset.chapter = chapter.id;

  const copy = el('div', 'scene-copy');
  copy.append(
    el('p', 'scene-kicker', { text: chapter.kicker }),
    el('h2', 'scene-title', { text: chapter.title }),
    el('p', 'scene-sub', { text: chapter.sub }),
  );

  const visualWrap = el('div', 'scene-visual');
  if (visual) visualWrap.append(visual);

  const actionsWrap = el('div', 'scene-actions');
  if (actions) actionsWrap.append(...(Array.isArray(actions) ? actions : [actions]));

  root.append(copy, visualWrap, actionsWrap);
  return { root, copy, visualWrap, actionsWrap };
}

export function choiceGroup(choices, { name, onSelect }) {
  const wrap = el('div', 'choices', { role: 'radiogroup', 'aria-label': name });
  const buttons = choices.map((c) => {
    const btn = el('button', 'choice-btn', { type: 'button', role: 'radio', 'aria-checked': 'false' });
    btn.dataset.id = c.id;
    const letter = el('span', 'letter', { text: c.letter });
    const text = el('span', '', { text: c.text });
    btn.append(letter, text);
    btn.addEventListener('click', () => {
      buttons.forEach((b) => {
        b.classList.remove('is-selected');
        b.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('is-selected');
      btn.setAttribute('aria-checked', 'true');
      onSelect?.(c.id, btn, buttons);
    });
    return btn;
  });
  wrap.append(...buttons);
  return wrap;
}
