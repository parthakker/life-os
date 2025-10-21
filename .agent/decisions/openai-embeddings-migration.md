# Migration Decision: OpenAI Embeddings API
## Date: October 20, 2025

---

## Problem Statement

**Out of Memory (OOM) crashes on Render**
- Render Starter plan: 512MB RAM limit
- Current usage: ~520MB (torch + sentence-transformers + bot)
- Result: Service crashes in loop, unusable in production

---

## Root Cause

**torch (PyTorch) dependency consuming 200-300MB**

Memory breakdown:
- Python + Telegram Bot: ~80MB
- **torch (PyTorch): ~200-300MB** ← Main culprit
- sentence-transformers model: ~90MB
- Model inference: ~50-100MB
- Database + other: ~20MB
- **TOTAL: ~490-540MB** → Exceeds 512MB limit

---

## Solution Options Considered

### Option A: Upgrade to Render Standard Plan
- **Cost:** $25/month (vs $7/month)
- **Memory:** 2GB
- **Pros:** Simple, immediate solution
- **Cons:** 3.5x more expensive

### Option B: Disable Auto-Vectorization
- **Cost:** $7/month
- **Pros:** Stays on cheap plan
- **Cons:** Manual maintenance, delayed searchability

### Option C: Remove RAG Entirely
- **Cost:** $7/month
- **Pros:** Minimal memory usage
- **Cons:** Loses core product value

### **Option D: Switch to OpenAI Embeddings API** ✅ **SELECTED**
- **Cost:** $7.37/month (~$0.01 for embeddings)
- **Memory:** ~110MB (78% reduction!)
- **Pros:** Better embeddings, lower cost, same functionality
- **Cons:** External API dependency (minimal)

---

## Selected Solution: OpenAI Embeddings API

### Technical Specifications

**Model:** text-embedding-3-small
- **Pricing:** $0.02 per 1M tokens
- **Default dimensions:** 1536
- **Our configuration:** 384 dimensions (to match all-MiniLM-L6-v2)
- **Performance:** Better than ada-002, 10%+ accuracy improvement

### Cost Analysis

**Current monthly cost:**
- Render Starter: $7.00/month
- Claude Haiku API: $0.36/month
- **Total: $7.36/month**

**After migration:**
- Render Starter: $7.00/month
- Claude Haiku API: $0.36/month
- OpenAI embeddings: ~$0.01/month
  - 100 messages/month
  - ~50 tokens per message average
  - 100 × 50 = 5,000 tokens/month
  - 5,000 ÷ 1,000,000 × $0.02 = $0.0001/month
- **Total: $7.37/month**

**Savings vs Upgrade:**
- Standard plan would be: $25.36/month
- Savings: $18/month = $216/year

### Memory Impact

**Before (torch + sentence-transformers):**
| Component | Memory |
|-----------|--------|
| Python + Telegram Bot | ~80MB |
| torch (PyTorch) | ~250MB |
| sentence-transformers model | ~90MB |
| Model inference | ~80MB |
| Database + other | ~20MB |
| **TOTAL** | **~520MB** ❌ (exceeds 512MB) |

**After (OpenAI API):**
| Component | Memory |
|-----------|--------|
| Python + Telegram Bot | ~80MB |
| OpenAI API client | ~10MB |
| numpy (for cosine similarity) | ~15MB |
| Database + other | ~20MB |
| **TOTAL** | **~125MB** ✅ (huge headroom!) |

**Memory reduction: 76%**

---

## Implementation Plan

### Dependencies Changed

**Removed:**
```txt
sentence-transformers==3.3.1
torch==2.5.1
```

**Added:**
```txt
openai==1.54.0
```

**Kept:**
```txt
numpy==2.0.2  # Still needed for cosine similarity
```

### Code Changes

**File modified:** `scripts/vector_store.py`

**Key changes:**
1. Replace SentenceTransformer import with OpenAI
2. Replace `get_embedding_model()` with `get_embedding(text)` API call
3. Remove lazy loading logic (not needed for API calls)
4. Update all `.encode()` calls to use OpenAI API
5. Re-vectorize all data with OpenAI embeddings

### Migration Steps

1. ✅ Research and document decision (this file)
2. Backup current implementation
3. Update requirements.txt
4. Rewrite vector_store.py
5. Set OPENAI_API_KEY environment variable
6. Re-vectorize all data locally
7. Test locally (imports, router, RAG, memory)
8. Deploy to Render
9. Test in production
10. Cleanup and documentation

---

## Risk Assessment

### Low Risk Factors
- ✅ Backing up before changes
- ✅ Testing locally first
- ✅ Can rollback to torch if needed
- ✅ OpenAI is reliable, production-grade service
- ✅ Minimal code changes (isolated to vector_store.py)

### Potential Issues & Mitigation

**Issue 1: API Rate Limits**
- **Likelihood:** Low
- **Mitigation:** text-embedding-3-small has 3000 RPM limit, we use ~1 request per message

**Issue 2: API Costs Higher Than Expected**
- **Likelihood:** Very Low
- **Mitigation:** Monitor first week, calculated <$1/month even at 10x usage

**Issue 3: Latency on Vectorization**
- **Likelihood:** Low
- **Mitigation:** OpenAI API is fast (~100ms), similar to local model

**Issue 4: Embedding Quality Different**
- **Likelihood:** Very Low
- **Mitigation:** OpenAI embeddings are BETTER than all-MiniLM

---

## Success Metrics

**Migration is successful when:**
- ✅ Render service memory: <200MB (vs 520MB before)
- ✅ No Out of Memory errors for 24+ hours
- ✅ RAG search returns relevant results
- ✅ Bot responds to Telegram messages
- ✅ Auto-vectorization works on new tasks/notes
- ✅ Service uptime: 99%+ (no crash loop)
- ✅ Monthly cost: ~$7.37 (confirmed via usage tracking)

---

## Rollback Plan

If migration fails, rollback steps:
1. `git revert` to previous commit
2. Restore `vector_store_torch_backup.py`
3. Restore `vector_store_torch_backup.json`
4. Restore old requirements.txt
5. Redeploy to Render
6. Consider Option A (upgrade to Standard plan)

---

## Conclusion

**OpenAI Embeddings API migration is the optimal solution:**
- ✅ Solves OOM problem permanently
- ✅ Maintains $7/month cost (vs $25 upgrade)
- ✅ Improves embedding quality
- ✅ Reduces maintenance (no local model management)
- ✅ Scales easily (OpenAI handles infrastructure)

**Approved for implementation.**

---

**Decision made by:** Claude Code + User
**Date:** October 20, 2025
**Status:** Ready for execution
