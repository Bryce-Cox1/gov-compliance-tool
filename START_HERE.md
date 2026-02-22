# 🚀 START HERE

**5-Minute Setup Guide**

---

## Step 1: Open Terminal

```bash
cd ~/.openclaw/workspace/gov-compliance-tool
```

---

## Step 2: Install Everything

Copy and paste this entire block:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
```

---

## Step 3: Add Your OpenAI API Key

1. Get a key from: https://platform.openai.com/api-keys
2. Open `.env` file (it's in this folder)
3. Replace `sk-your-api-key-here` with your actual key
4. Save the file

**Don't have a key yet?** The tool will still work for scoring (just no rewriting).

---

## Step 4: Test Everything Works

```bash
python test_setup.py
```

If you see "✅ ALL TESTS PASSED!" → you're ready!

---

## Step 5: Start the Server

```bash
python app.py
```

**Then open your browser to:** http://localhost:8000

---

## 🎯 What To Do Next

1. **Paste some government text** (grab from any .gov.au site)
2. **Click "Analyze & Rewrite"**
3. **See the magic happen**
4. **Test with 5-10 different samples**

**Goal:** Validate that the scores are accurate and rewrites are good.

---

## 💡 Quick Test Samples

### Bad Example (Should Score High Grade)
```
The application should be submitted by the applicant to the relevant 
department prior to the commencement of the assessment process. It is 
imperative that all required documentation is provided in accordance 
with the stipulated requirements.
```

### Good Example (Should Score Grade 7-8)
```
Submit your application to the department before we start assessing. 
Make sure you include all required documents as listed.
```

Paste both and compare the scores!

---

## 🐛 Troubleshooting

**"Module not found" error?**
- Run: `pip install -r requirements.txt`

**"spaCy model not found"?**
- Run: `python -m spacy download en_core_web_sm`

**"API key not configured"?**
- Edit `.env` file and add your OpenAI key
- Restart the server

**Still broken?**
- Check `README.md` for detailed troubleshooting
- Or just message me (Rook) and I'll help

---

## 📊 Next Steps (After Testing)

Once you've validated the tool works:

1. **Test with 10-20 real gov docs** (collect good/bad examples)
2. **Show it to 5 gov content people** (get their feedback)
3. **Decide:** Is this solving a real problem?
4. **Then:** We build the full product (accounts, payments, deployment)

But first: **Validate the core tech works!**

---

**That's it! You've got this. 🚀**

*Built by Rook ♟️ in 45 minutes*
