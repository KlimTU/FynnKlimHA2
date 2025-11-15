<script>
  import "./app.css";
  import Spinner from "./lib/spinner.svelte";

  let notes = [];
  let title = "";
  let body = "";
  let search = "";
  let deleteId = "";
  let sortOption = "created_at";

  let titleError = false;
  let bodyError = false;
  let idError = false;

  let loading = false;

  function flashError(fields, duration = 700) {
    // fields = Array von Referenzen auf Error-Flags, z.B. [() => titleError = true, ...]
    fields.forEach((setter) => setter(true));
    setTimeout(() => fields.forEach((setter) => setter(false)), duration);
  }

  async function fetchNotes() {
    loading = true;
    try {
      let url = "/api/items";

      if (search) {
        if (!isNaN(Number(search)) && Number.isInteger(Number(search))) {
          url = `/api/items/${Number(search)}`;
        } else {
          url += `?q=${encodeURIComponent(search)}&sort=${encodeURIComponent(sortOption)}`;
        }
      } else if (sortOption) {
        url += `?sort=${encodeURIComponent(sortOption)}`;
      }

      const res = await fetch(url);
      if (!res.ok) throw new Error("Fehler beim Laden der Notizen");

      if (url.includes("/api/items/") && !url.includes("?")) {
        notes = [await res.json()];
      } else {
        notes = await res.json();
      }
    } catch (err) {
      console.error(err);
      notes = [];
    } finally {
      loading = false;
    }
  }

  async function addNote() {
    const errorFields = [];

    if (!title.trim()) errorFields.push((v) => (titleError = v));
    if (!body.trim()) errorFields.push((v) => (bodyError = v));

    if (errorFields.length > 0) {
      flashError(errorFields);
      return;
    }

    loading = true;
    try {
      const res = await fetch("/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, body }),
      });
      if (!res.ok) {
        const data = await res.json();
        console.error("Fehler:", data);
        return;
      }
      await fetchNotes();
      title = "";
      body = "";
    } catch (err) {
      console.error(err);
    } finally {
      loading = false;
    }
  }

  async function deleteNote() {
    const idNum = Number(deleteId);
    if (
      !deleteId.trim() ||
      isNaN(idNum) ||
      !Number.isInteger(idNum) ||
      idNum <= 0
    ) {
      flashError([(v) => (idError = v)]);
      return;
    }
    loading = true;
    try {
      const res = await fetch(`/api/items/${idNum}`, { method: "DELETE" });
      if (res.status === 404) {
        flashError([(v) => (idError = v)]);
        return;
      } else if (!res.ok) {
        throw new Error("Fehler beim Löschen");
      }
      await fetchNotes();
      deleteId = "";
    } catch (err) {
      console.error(err);
    } finally {
      loading = false;
    }
  }

  // Re-fetch notes whenever search or sortOption changes
  $: if (search !== undefined || sortOption !== undefined) {
    fetchNotes();
  }
</script>

<h1>Simple persistente Notizen-App</h1>

<!-- new note input -->
<div class="input-container">
  <input
    bind:value={title}
    placeholder="Titel"
    class:title-error={titleError}
  />

  <input bind:value={body} placeholder="Inhalt" class:body-error={bodyError} />

  <button on:click={addNote}>Notiz Hinzufügen</button>
</div>

<!-- delete input -->
<div class="input-container">
  <input
    bind:value={deleteId}
    placeholder="ID der zu löschenden Notiz"
    class:id-error={idError}
  />
  <button on:click={deleteNote}>Notiz Löschen</button>
</div>

<!-- search input -->
<div class="input-container">
  <input bind:value={search} placeholder="Suche nach ID/Titel/Inhalt..." />
</div>

<!-- sort menu -->
<div class="sort-container">
  <label for="sort-select">Sortierung:</label>
  <select id="sort-select" bind:value={sortOption}>
    <option value="created_at">Erstellt (aufsteigend)</option>
    <option value="-created_at">Erstellt (absteigend)</option>
    <option value="title">Titel (A-Z)</option>
    <option value="-title">Titel (Z-A)</option>
    <option value="id">ID (aufsteigend)</option>
    <option value="-id">ID (absteigend)</option>
  </select>
</div>

<!-- grid always only shows notes when not loading -->
<div class="notes-table">
  <div class="notes-header">
    <div class="col id">ID</div>
    <div class="col date">Erstelldatum</div>
    <div class="col title">Titel</div>
    <div class="col body">Inhalt</div>
  </div>
  {#if loading}
    <Spinner size={20} color="#555" />
  {:else}
    {#each notes as n}
      <div class="note-row">
        <div class="col id">{n.id}</div>
        <div class="col date">
          {new Date(n.created_at).toLocaleString("de-DE", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
        <div class="col title">{n.title}</div>
        <div class="col body">{n.body}</div>
      </div>
    {/each}
  {/if}
</div>
