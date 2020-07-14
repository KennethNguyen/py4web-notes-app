// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        notes: [],
        add_note_text: "",
        add_note_title: "",
        form_visible: false,
        color: "white"
    };

    app.index = (a) => {
        let i = 0;
        for (let p of a) {
            p._idx = i++;
            p.edit = false;
            p.original_title = p.note_title; // Title before an edit.
            p.server_title = p.note_title; // Title on the server.
            p.original_text = p.note_text; // Text before an edit.
            p.server_text = p.note_text; // Text on the server.
        }
        return a;
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map(e => {e._idx = k++});
        return a;
    };
            /*
            app.enumerate(notes);
            app.vue.notes = notes
            */
    app.add_note = () => {
        app.perform_insertion();
        app.init();
    };

    app.perform_insertion = () => {
        axios.post(add_note_url, {
            note_text: app.vue.add_note_text,
            note_title: app.vue.add_note_title
        }).then(function (response) {
            app.vue.notes.push({
                id: response.data.id,
                note_text: app.vue.add_post_text,
                note_title: app.vue.add_note_title
            });
        });
        app.data.add_note_text = "";
        app.data.add_note_title = "";
    };

    app.delete_note = (note_idx) => {
        let p = app.vue.notes[note_idx];
        axios.post(delete_note_url, {id: p.id}).then(() => {
            app.vue.notes.splice(note_idx, 1);
            app.enumerate(app.vue.notes);
        })
    };

    app.set_star = (note_idx, star_status) => {
        let this_note = app.vue.notes[note_idx];
        this_note.important = star_status;
        axios.post(set_star_url, {
            note_id: this_note.id, 
            important: star_status,
        });
        app.init();
    }

    app.set_color = (note_idx, color_status) => {
        let this_note = app.vue.notes[note_idx];
        this_note.color = this_note.color == color_status ? 'white' : color_status;
        axios.post(set_color_url, {
            note_id: this_note.id, 
            color: this_note.color,
        });
        app.init();
    }

    app.do_edit = (note_idx) => {
        let p = app.vue.notes[note_idx];
        p.edit = true;
    };

    app.do_cancel = (note_idx) => {
        // Handler for button that cancels the edit.
        let p = app.vue.notes[note_idx];
        p.edit = false;
        p.note_title = p.original_title;
        p.note_text = p.original_text;
    }

    app.do_save = (note_idx) => {
        // Handler for "Save edit" button.
        let p = app.vue.notes[note_idx];
        if (p.note_text == "" || p.note_title == "") { throw("Saved post must not be blank"); }
        if (p.note_text !== p.server_text || p.note_title !== p.server_title) {
            axios.post(get_notes_url, {
                note_title: p.note_title,
                note_text: p.note_text,
                note_id: p.id,
            }).then((result) => {
                p.original_text =
                    p.server_text =
                        result.data.note_text;
                p.original_title =
                        p.server_title =
                            result.data.note_title;
                p.id = result.data.note_id;
                p.edit = false;
            }).catch( () => {
                alert("Unable to save post, please try again");
                // We stay in edit mode.
            });
        } else {
            // No need to save.
            p.edit = false;
            p.note_text = p.original_text;
            p.note_title = p.original_title;
        }
        app.init()
    }

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        add_note: app.add_note,
        delete_note: app.delete_note,
        init: app.init,
        set_star: app.set_star,
        set_color: app.set_color,
        do_edit: app.do_edit,
        do_save: app.do_save,
        do_cancel: app.do_cancel,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(get_notes_url).then((result) => {
            let notes = result.data.notes;
            app.vue.notes = app.index(notes);
        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
