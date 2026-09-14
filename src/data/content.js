/** Source-aligned lesson content. Do not contradict docs/CONTENT_MAP.md */

export const CHAPTERS = [
  {
    id: 'mystery',
    label: 'Mystery',
    kicker: 'Chapter 01',
    title: 'What does a flame need to keep burning?',
    sub: 'Air is all around us — invisible, but powerful. Tonight we investigate its role in fire.',
  },
  {
    id: 'air',
    label: 'Invisible Air',
    kicker: 'Chapter 02',
    title: 'Air is everywhere.',
    sub: 'You cannot see it. But can something invisible affect a flame?',
  },
  {
    id: 'experiment',
    label: 'Experiment',
    kicker: 'Chapter 03',
    title: 'Build the investigation.',
    sub: 'Wooden board, clay, candle, bottomless glass jar, metal lid — and a lighter used only by the teacher.',
  },
  {
    id: 'prediction',
    label: 'Predict',
    kicker: 'Chapter 04',
    title: 'What do you think will happen?',
    sub: 'If we seal the jar with a metal lid, what happens to the flame?',
  },
  {
    id: 'closed',
    label: 'Closed Jar',
    kicker: 'Chapter 05',
    title: 'Trap the air.',
    sub: 'Close the jar. Watch what happens to the invisible air inside — and to the flame.',
  },
  {
    id: 'out',
    label: 'Goes Out',
    kicker: 'Chapter 06',
    title: 'The flame goes out.',
    sub: 'The flame gradually weakens… then the candle goes out after a short time.',
  },
  {
    id: 'why',
    label: 'Why?',
    kicker: 'Chapter 07',
    title: 'The air inside was used up.',
    sub: 'In a closed jar, the air is used up. Once it runs out, the candle goes out.',
  },
  {
    id: 'fresh',
    label: 'Fresh Air',
    kicker: 'Chapter 08',
    title: 'Fresh air in. Warm air out.',
    sub: 'With a gap at the bottom and an opening at the top, air is constantly renewed.',
  },
  {
    id: 'aha',
    label: 'Aha',
    kicker: 'Chapter 09',
    title: 'Closed vs. airflow.',
    sub: 'Side by side: sealed air runs out. Continuous fresh air keeps burning going.',
  },
  {
    id: 'science',
    label: 'Science',
    kicker: 'Chapter 10',
    title: 'What is meant by burning?',
    sub: 'Burning (combustion) is a reaction between oxygen and a substance that produces heat and light.',
  },
  {
    id: 'world',
    label: 'Real World',
    kicker: 'Chapter 11',
    title: 'Where do we see this?',
    sub: 'Candles, fireplaces, stoves, engines — burning needs a continuous supply of fresh air.',
  },
  {
    id: 'challenge',
    label: 'Challenge',
    kicker: 'Chapter 12',
    title: 'Which candle burns longer?',
    sub: 'Two setups. Use what you discovered about openings and fresh air.',
  },
  {
    id: 'discovery',
    label: 'Discovery',
    kicker: 'Final',
    title: 'Air plays an important role in burning.',
    sub: 'Fresh air must continuously be supplied for burning to continue.',
  },
];

export const PREDICTION_CHOICES = [
  { id: 'a', letter: 'A', text: 'The flame keeps burning the same.' },
  { id: 'b', letter: 'B', text: 'The flame becomes weaker, then may go out.' },
  { id: 'c', letter: 'C', text: 'The flame goes out right away.' },
];

/** Closest scientifically to Step 3 observation: gradually weakens, then goes out. */
export const PREDICTION_BEST = 'b';

export const CHALLENGE_CHOICES = [
  {
    id: 'sealed',
    letter: 'A',
    text: 'Candle A — jar sealed with a lid, no gaps.',
  },
  {
    id: 'bottom',
    letter: 'B',
    text: 'Candle B — lid on, but a small gap only at the bottom.',
  },
  {
    id: 'both',
    letter: 'C',
    text: 'Candle C — gap at the bottom and open at the top.',
  },
];

/** Step 5 continues; Step 3 & 4 go out (4 lasts slightly longer than 3). */
export const CHALLENGE_BEST = 'both';

export const CONCLUSIONS = [
  'Air has a role in burning.',
  'One of the most important conditions for things to continue burning is that fresh air must constantly flow in and out.',
  'In a place where air is not renewed, things cannot continue burning.',
];

export const SAFETY =
  'Caution: Only the teacher should use the lighter to light the candle.';

export const MATERIALS = [
  { id: 'board', name: 'Wooden board' },
  { id: 'clay', name: 'Clay' },
  { id: 'candle', name: 'Candle' },
  { id: 'jar', name: 'Bottomless glass jar' },
  { id: 'lid', name: 'Metal lid' },
  { id: 'lighter', name: 'Lighter (teacher only)' },
];

export const REAL_WORLD = [
  {
    id: 'candle',
    title: 'Candle',
    text: 'A candle needs surrounding air. Cover it tightly and the flame cannot continue.',
  },
  {
    id: 'fireplace',
    title: 'Fireplace',
    text: 'Chimneys let warm air rise out so fresh air can flow in to feed the fire.',
  },
  {
    id: 'stove',
    title: 'Gas stove',
    text: 'Burners are designed so air can mix with fuel for a steady flame.',
  },
  {
    id: 'engine',
    title: 'Engine',
    text: 'Engines take in air so fuel can burn and release energy.',
  },
];
