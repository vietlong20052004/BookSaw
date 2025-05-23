# 📚 Online Library Web App

 Users can browse, search, borrow, return, review, and rate books. Staff users can manage books, approve/reject borrow requests, view audit logs, and send in-app notifications.

---

## 🚀 Features

### Authentication & Authorization
- **User roles:**  
  - **Staff:** full CRUD on books/authors/categories, manage users and borrows, view audit logs, send notifications  
  - **User:** browse, search, filter, borrow/return books, view loan history, rate & review, see notifications  
- **Signup / Login / Logout** flows  
- Permissions enforced at view & template level

### Books
- **Book** model: title, description, ISBN, year, publisher, language, M2M authors & categories, cover image  
- Daily / monthly / yearly view counters  
- “Recently added” slider on homepage

### Borrowing & Returns
- **BorrowRequest** workflow: user “requests” → staff approves/rejects → on approve, a **Loan** is created, copy marked unavailable  
- Admin can pick custom due date in the Django admin form  
- **Loan** model: borrow date, due date, returned date, `is_overdue` property  
- User “My Loans” dashboard shows pending requests, active loans (with Return button), overdue & returned status  
- Return action marks copy available again, records return date, sends notification

### Reviews & Ratings
- Logged-in users rate (1–5) and review books  
- Each user can post one review per book  
- Reviews sorted by number of likes/dislikes 
- Like/dislike action

### Notifications
- In-app bell icon shows unread count  
- Dropdown lists recent notifications with timestamp  
- Notifications are created for: borrow request pending, approval, rejection, return confirmation, review/like events  
- Clicking a notification marks it read and redirects to the relevant page


