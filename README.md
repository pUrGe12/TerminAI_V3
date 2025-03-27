# TerminAI_V3


## Installing and running

This project depends on poetry. To install the necessary dependencies and run TerminAI

		poetry run python3 terminai.py

To add a certain dependency, run

		poetry add <name>

---

## About

A python based terminal with AI capabilities, line of thought and history.

Improvements over version 2:
- [ ] Better history management (supabase was overkill and not necessary) we can make do with in-memory history. (comparitively easier)
- [ ] Use vector embeddings for commands and description and retrieving that then passing to the LLM. (uhh, I have no idea how to do this, described below)

Every command has a `man` page, we can use that to generate a `hybrid vector DB` which means, we're storing the command, its descrption, its flags and their descriptions.

That's a lot of data!

Now based on the user's query, we embed that using Vertex AIs models. 

Can we have like 3 interlinked databases, I push my query into one of them and trace it back to the command?

Can I have multiple databases??!! This will then be the structure


```

(command )_db -> (descrption)_db; (description)_db -> (description_i)_db -> (flags)_db -> (description)_db

```

![Flow diagram with LVS](./images/TerminAI_V3.png)


The explicit parts of LVS are as shown below:

![LVS parts](./images/linked_vector_system_parts.png)

---

## Creating a vDB

TBD

---