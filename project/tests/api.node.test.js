import { test } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { app, db } from '../server.js';

test('API health and notes flow', async (t) => {
  // start server on ephemeral port
  const srv = app.listen(0);
  await once(srv, 'listening');
  const port = srv.address().port;
  const base = `http://127.0.0.1:${port}`;

  try {
    // health
    let res = await fetch(base + '/api/health');
    assert.equal(res.status, 200);
    let body = await res.json();
    assert.equal(body.status, 'ok');

    // clear notes
    await new Promise((resolve, reject) => db.run('DELETE FROM notes', (e) => e ? reject(e) : resolve()));

    // get notes (should be empty)
    res = await fetch(base + '/api/notes');
    assert.equal(res.status, 200);
    body = await res.json();
    assert.ok(Array.isArray(body));
    assert.equal(body.length, 0);

    // create note
    res = await fetch(base + '/api/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: 'node-test note' })
    });
    assert.equal(res.status, 201);
    body = await res.json();
    assert.ok(body.id);

    // get notes (should contain at least one)
    res = await fetch(base + '/api/notes');
    assert.equal(res.status, 200);
    body = await res.json();
    assert.ok(body.length >= 1);
  } finally {
    srv.close();
    // close DB
    await new Promise((r) => db.close(r));
  }
});
