/* supabase.js — shared Supabase access
   New project? Replace only the two lines below (Supabase -> Settings -> API). */

const SUPABASE_URL  = 'https://gjjtwoigivdrbfweymkd.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdqanR3b2lnaXZkcmJmd2V5bWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgzMzkwNDYsImV4cCI6MjEwMzkxNTA0Nn0.rL34QKxjXKFPRTRB6-HYUQYPfCIeu9OViPbvtRU3Bgg';

/* Safe mode when the CDN is blocked: every query resolves with an error instead
   of throwing, so the pages still render their defaults. */
const SB_READY = typeof supabase !== 'undefined';
const db = SB_READY ? supabase.createClient(SUPABASE_URL, SUPABASE_ANON, {
  auth: { persistSession: true, autoRefreshToken: true, storageKey: 'shuni-auth' }
}) : {
  auth: {
    getSession: function () { return Promise.resolve({ data: { session: null } }); },
    signInWithPassword: function () { return Promise.resolve({ error: { message: '키 미설정' } }); },
    signOut: function () { return Promise.resolve({}); }
  },
  from: function () {
    const q = {
      select: () => q, order: () => q, limit: () => q, eq: () => q,
      insert: () => q, update: () => q, delete: () => q,
      then(res) { res({ data: null, error: { message: '키 미설정' } }); }
    };
    return q;
  }
};

/** 전체 조회 — fetchAll('schedule', { order:'date', asc:true }) */
async function fetchAll(table, options = {}) {
  let query = db.from(table).select('*');
  if (options.order)  query = query.order(options.order, { ascending: options.asc ?? false });
  if (options.limit)  query = query.limit(options.limit);
  if (options.filter) query = query.eq(options.filter.col, options.filter.val);
  const { data, error } = await query;
  if (error) { console.error(`fetchAll(${table})`, error); return []; }
  return data || [];
}

/** 단건 삽입 */
async function insertRow(table, row) {
  const { error } = await db.from(table).insert(row);
  if (error) { console.error(`insertRow(${table})`, error); return false; }
  return true;
}

/** 삽입 후 생성된 행 반환 — 새 id가 바로 필요할 때 */
async function insertRowReturning(table, row) {
  const { data, error } = await db.from(table).insert(row).select();
  if (error) { console.error(`insertRowReturning(${table})`, error); return null; }
  return (data && data[0]) || null;
}

/** 단건 수정 */
async function updateRow(table, id, updates) {
  const { error } = await db.from(table).update(updates).eq('id', id);
  if (error) { console.error(`updateRow(${table})`, error); return false; }
  return true;
}

/** 단건 삭제 */
async function deleteRow(table, id) {
  const { error } = await db.from(table).delete().eq('id', id);
  if (error) { console.error(`deleteRow(${table})`, error); return false; }
  return true;
}
