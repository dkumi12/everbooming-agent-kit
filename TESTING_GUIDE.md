# Testing Guide for Updated Prompts

## Quick Test Checklist

### Test Product Idea
Use a simple, well-defined product to test all improvements:

**Example Test Input:**
```
Product Idea: A mobile app that helps freelance developers track 
their time across multiple projects, generate invoices automatically, 
and provide insights on their hourly rates and productivity patterns.
```

This idea should trigger:
- ✅ Clear user personas (freelance developers)
- ✅ Database schema (projects, time_entries, invoices tables)
- ✅ API endpoints (POST /time-entries, GET /invoices, etc.)
- ✅ NFRs (mobile performance, security for financial data)
- ✅ Story points estimation (simple CRUD vs complex analytics)
- ❌ AI/ML components (unless we add "AI-powered rate suggestions")

### What to Check in Each Output

#### 1. Business Analysis (`outputs/ba.md`)
Look for:
- [ ] At least 2 complete personas with all fields filled
- [ ] Age, occupation, tech savviness, goals, pain points for each
- [ ] Realistic quotes that capture user needs
- [ ] No "TBD" or placeholder text

#### 2. System Architecture (`outputs/arch.md`)
Look for:
- [ ] Complete database schema with:
  - Column names, types, and constraints
  - Primary/Foreign key relationships
  - Index recommendations
- [ ] API endpoints with method, path, request/response format
- [ ] Tech stack with cloud provider alternatives
- [ ] Folder structure (not just "backend/" but actual subdirectories)
- [ ] AI/ML section (even if "Not applicable for this product")

#### 3. PRD (`outputs/prd.md`)
Look for:
- [ ] NFRs with specific numbers:
  - "API response < 200ms" not "fast responses"
  - "99.9% uptime" not "high availability"
  - "Support 1000 concurrent users" not "scalable"
- [ ] User flows with step-by-step format
- [ ] Edge cases with EC-001, EC-002 format
- [ ] Acceptance criteria with Given-When-Then format

#### 4. Sprint Plan (`outputs/sm.md`)
Look for:
- [ ] Story point estimates (1, 2, 3, 5, 8, 13)
- [ ] Total points per sprint (should be 20-25)
- [ ] Sprint goals (one sentence per sprint)
- [ ] Key deliverables listed
- [ ] Sprint summary with total points and duration

## Running the Test

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Enter the test product idea** (use the example above)

3. **Run the full pipeline** (all 7 agents)

4. **Download the outputs** (both PDF and ZIP)

5. **Review using the checklist above**

## Expected Improvements

### Database Schema (Before → After)
**Before:**
```
Database: PostgreSQL
Tables: users, projects, time_entries
```

**After:**
```
### Table: time_entries
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| project_id | UUID | FK to projects | Associated project |
| user_id | UUID | FK to users | Freelancer who logged time |
| start_time | TIMESTAMP | NOT NULL | When work started |
| end_time | TIMESTAMP | NOT NULL | When work ended |
| duration_minutes | INTEGER | NOT NULL | Calculated duration |
| hourly_rate | DECIMAL(10,2) | NOT NULL | Rate for this entry |
| notes | TEXT | NULLABLE | Description of work |
| created_at | TIMESTAMP | DEFAULT NOW() | Entry creation time |

**Relationships:**
- N:1 with projects (project_id)
- N:1 with users (user_id)

**Indexes:**
- idx_user_date ON time_entries(user_id, start_time) for timeline queries
- idx_project ON time_entries(project_id) for project reports
```

### NFRs (Before → After)
**Before:**
```
- Fast performance
- Secure data
- Available 24/7
```

**After:**
```
### Performance
- Mobile app launch time < 2 seconds
- Time entry creation < 500ms
- Invoice generation < 3 seconds for 100 entries
- Offline mode: Store up to 1000 entries locally

### Security
- Authentication: OAuth 2.0 with JWT tokens
- Data encryption: AES-256 at rest, TLS 1.3 in transit
- Compliance: GDPR for EU users, store data in user's region
- API rate limiting: 100 requests/minute per user
- Automatic session timeout after 30 minutes of inactivity

### Scalability
- Launch target: 500 active freelancers
- 12-month projection: 5,000 users
- Database partitioning by user_id for horizontal scaling
- CDN for static assets

### Availability
- SLA: 99.5% uptime (43.8 hours downtime/year maximum)
- Backup: Hourly incremental, daily full backups
- Disaster recovery: RPO 1 hour, RTO 4 hours
- Maintenance window: Sundays 2-4 AM UTC
```

### Story Points (Before → After)
**Before:**
```
Sprint 1:
- Set up database
- Create API
- Build UI
```

**After:**
```
### Sprint 1: Foundation (Total: 24 points)

| ID | Story | Points | Priority |
|----|-------|--------|----------|
| US-001 | Set up PostgreSQL schema with all tables | 5 | High |
| US-002 | Implement user authentication (OAuth) | 8 | High |
| US-003 | Create time entry CRUD API endpoints | 5 | High |
| US-004 | Build project management API | 3 | High |
| US-005 | Set up React Native development environment | 3 | High |

**Sprint Goal:** Deliver backend infrastructure and authentication system
**Key Deliverables:** Working API, database, user auth, dev environment ready
```

## Success Criteria

The updated prompts are successful if:
1. ✅ No empty sections in any output file
2. ✅ Database schema includes at least 3 complete table definitions
3. ✅ NFRs have at least 5 specific, measurable targets
4. ✅ Sprint plan has story points totaling 60-75 across 3 sprints
5. ✅ PDF export is readable and professionally formatted

## Failure Indicators

Watch out for:
- ❌ "TBD" or "[to be determined]" in any section
- ❌ Database schema with only table names, no columns
- ❌ NFRs with vague terms like "fast", "secure", "reliable"
- ❌ Sprint stories without point estimates
- ❌ Sections that say "This will be detailed later"

## Next Steps After Testing

If test passes:
1. Test with a more complex product (e.g., AI-powered social platform)
2. Verify AI/ML section appears when relevant
3. Consider implementing model selection per agent

If test fails:
1. Check which prompts still produce empty sections
2. Add even more explicit examples in the prompt
3. Consider adding validation logic in the agent scripts

---

**Quick Command to Test:**
```bash
# From project root
streamlit run app.py

# Test idea: "A mobile app for freelance developers to track time and generate invoices"
# Expected runtime: 3-5 minutes for all 7 agents
# Expected output size: 15-25 pages in PDF
```
