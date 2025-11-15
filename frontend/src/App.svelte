<script>
  import "./app.css";
  import Spinner from "./lib/spinner.svelte";

  let notes = [];

  let nextID = 1;
  let title = "";
  let content = "";
  let search = "";
  let deleteId = "";

  let titleError = false;
  let contentError = false;
  let idError = false;

  let loading = false;

  function flashError(setter, duration = 700) {
    setter(true);
    setTimeout(() => setter(false), duration);
  }

  // adds note if it has no empty fields for title and content
  function addNote() {
    const titleMissing = !title.trim();
    const contentMissing = !content.trim();

    if (titleMissing) flashError((v) => (titleError = v));
    if (contentMissing) flashError((v) => (contentError = v));

    if (!titleMissing && !contentMissing) {
      const newNote = {
        id: nextID++,
        created_at: new Date().toLocaleString(),
        title,
        content,
      };

      notes = [...notes, newNote];
      title = "";
      content = "";
    }
  }

  // deletes a note by ID with live validation
  function deleteNote() {
    if (!deleteId.trim()) {
      flashError((v) => (idError = v));
      return;
    }

    const idNum = Number(deleteId);
    const exists = notes.some((n) => n.id === idNum);

    if (!exists) {
      flashError((v) => (idError = v));
      return;
    }

    notes = notes.filter((n) => n.id !== idNum);
    deleteId = "";
  }

  // case insensitive search
  $: filteredNotes = notes.filter(
    (n) =>
      n.title.toLowerCase().includes(search.toLowerCase()) ||
      n.content.toLowerCase().includes(search.toLowerCase()) ||
      n.id.toString().includes(search) ||
      n.created_at.includes(search)
  );
</script>

<h1>Simple persistente Notizen-App</h1>

<!-- new note input -->
<div class="input-container">
  <input
    bind:value={title}
    placeholder="Titel"
    class:title-error={titleError}
  />

  <input
    bind:value={content}
    placeholder="Inhalt"
    class:content-error={contentError}
  />

  <button on:click={addNote}>Hinzufügen</button>
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
  <input bind:value={search} placeholder="Suche..." />
</div>

<!-- grid always only shows filteredNotes when not loading -->
<div class="notes-table">
  <div class="notes-header">
    <div class="col id">ID</div>
    <div class="col date">Erstelldatum</div>
    <div class="col title">Titel</div>
    <div class="col content">Inhalt</div>
  </div>
  {#if loading}
    <Spinner size={20} color="#555" />
  {:else}
    {#each filteredNotes as n}
      <div class="note-row">
        <div class="col id">{n.id}</div>
        <div class="col date">{n.created_at}</div>
        <div class="col title">{n.title}</div>
        <div class="col content">{n.content}</div>
      </div>
    {/each}
  {/if}
</div>
