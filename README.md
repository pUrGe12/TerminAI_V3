# TerminAI_V3

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

In words:

I have a commands vector DB. Each command in there is `linked` to its description in the description database. Each description is linked to a flags database, which essentially stores all the flags for that particular description. Each flag in the flag database is then linked to each description in the flag_description database (which must be equal to the number of flag databases).

Then when the user creates a prompt, we embed that, pass it into the flag desc DBs (all of them) and description DB. Then we backtract using the links to the commands and select the best ones (along with the right flags)

Pass that to the gemini model and give it the prompt, tell it to figure out the best command for the job. 

THIS WILL BE MUCH RELIABLE.