# 🎯 The Proper Noun Problem

**Issue:** Government text scores poorly even when written simply, because mandatory proper nouns inflate the reading grade.

---

## 📊 Example

**Text:**
```
To qualify for the black coal mining industry long service leave scheme, 
we look at your job and what you do.
```

**Flesch-Kincaid Score:** Grade 11.2

**Why?**
- "black coal mining industry long service leave scheme" = complex proper noun
- Can't simplify it (it's the official name)
- But formula counts all those syllables

---

## 🔍 What We Need

**Context-aware scoring:**

1. **Detect proper nouns:**
   - Act names: "Coal Mining Industry (Long Service Leave) Administration Act 1992"
   - Scheme names: "black coal mining industry long service leave scheme"
   - Department names: "Department of Infrastructure, Transport, Regional Development..."
   - Location names: "New South Wales", "Australian Capital Territory"

2. **Exclude from calculation:**
   - Calculate grade WITH proper nouns
   - Calculate grade WITHOUT proper nouns
   - Show both scores

3. **Rewrite targets:**
   - Don't try to simplify proper nouns
   - Focus on the surrounding text

---

## 📐 Math Example

**Original calculation:**
```
Total words: 24
Total syllables: 42
Grade = 0.39 × (24/2) + 11.8 × (42/24) - 15.59
     = 0.39 × 12 + 11.8 × 1.75 - 15.59
     = 4.68 + 20.65 - 15.59
     = 9.74
```

**If we exclude "black coal mining industry long service leave scheme":**
```
Content words: 17
Content syllables: 22
Grade = 0.39 × (17/2) + 11.8 × (22/17) - 15.59
     = 0.39 × 8.5 + 11.8 × 1.29 - 15.59
     = 3.32 + 15.22 - 15.59
     = 2.95  ← Much better!
```

---

## 🚀 Implementation Plan

### Phase 1: Detection
```python
import spacy

nlp = spacy.load("en_core_web_sm")

def detect_proper_nouns(text):
    doc = nlp(text)
    proper_nouns = []
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "LAW", "GPE", "PRODUCT"]:
            proper_nouns.append(ent.text)
    
    # Also detect Act names via regex
    act_pattern = r'\b\w+.*?Act\s+\d{4}\b'
    acts = re.findall(act_pattern, text)
    proper_nouns.extend(acts)
    
    return proper_nouns
```

### Phase 2: Dual Scoring
```python
def score_with_context(text):
    proper_nouns = detect_proper_nouns(text)
    
    # Score 1: Full text (what we show now)
    full_score = calculate_grade(text)
    
    # Score 2: Content only (exclude proper nouns)
    content_text = text
    for noun in proper_nouns:
        content_text = content_text.replace(noun, "")
    content_score = calculate_grade(content_text)
    
    return {
        'full_grade': full_score,
        'content_grade': content_score,
        'proper_nouns': proper_nouns,
        'note': 'Content grade excludes unavoidable proper nouns'
    }
```

### Phase 3: Smart Rewriting
```python
def smart_rewrite(text):
    proper_nouns = detect_proper_nouns(text)
    
    prompt = f"""
Rewrite this text to Grade 7 reading level.

DO NOT simplify these proper nouns (they're official terms):
{chr(10).join(f'• {noun}' for noun in proper_nouns)}

Simplify everything else.
"""
```

---

## 🎯 Expected Results

**Before:**
```
Reading Grade: 11.2
Message: "Failed - too complex"
```

**After:**
```
Reading Grade (full): 11.2
Reading Grade (content): 6.8 ✓
Proper nouns detected: 2 (unavoidable)
Message: "Content meets Grade 7 target. Grade inflated by mandatory proper nouns."
```

---

## 🤔 Trade-offs

**Option A: Show dual scores**
- Pro: Honest about limitations
- Pro: Content writers see what they can control
- Con: More complex to explain

**Option B: Adjust target for proper nouns**
- Pro: Simpler interface
- Pro: Realistic expectations
- Con: Hides the problem

**Option C: Warn about proper nouns**
- Pro: Quick fix
- Pro: Educates users
- Con: Doesn't solve scoring issue

**Recommendation:** Option A (dual scoring)

---

## 📚 AGSM Guidance

**From the Style Manual:**

> "Use plain language where possible. When technical terms or proper nouns 
> are unavoidable, ensure the surrounding text is as simple as possible."

**Our tool should:**
- Accept that some terms can't be simplified
- Focus on making everything ELSE readable
- Report on what's within user control

---

## 🧪 Test Cases

**Test 1: Department name**
```
Input: "The Department of Infrastructure, Transport, Regional Development, 
        Communications and the Arts manages programs."
        
Proper nouns: "Department of Infrastructure, Transport, Regional Development, 
               Communications and the Arts"
               
Content: "manages programs"
Content grade: 5.2 ✓
```

**Test 2: Act reference**
```
Input: "You can find details in the Coal Mining Industry (Long Service Leave) 
        Administration Act 1992."
        
Proper nouns: "Coal Mining Industry (Long Service Leave) Administration Act 1992"
Content: "You can find details in the"
Content grade: 3.1 ✓
```

**Test 3: No proper nouns**
```
Input: "You must send your form before the deadline."
Content grade: 4.8 ✓
```

---

## 🚧 Next Steps

1. Add spaCy named entity recognition
2. Build proper noun detector (entities + regex for Acts)
3. Implement dual scoring
4. Update UI to show both scores
5. Update rewrite prompts to exclude proper nouns
6. Test with 20 real gov documents

---

**This is a critical fix for government text compliance checking.**

Without it, we'll always show "failing" scores on perfectly good text that just happens to reference Act names or scheme titles.
