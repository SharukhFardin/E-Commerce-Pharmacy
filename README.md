# E-Commerce-Pharmacy
Django &amp; DRF-based backend code for a Pharmacy E-Commerce Website.

E-commerce Pharmacy Website (Backend):

1. Introduction
Project Objective
The primary objective of this project is to develop a robust E-commerce website for a pharmacy
shop. The website will facilitate the selling of medicines to customers, provide inventory management
tools, and enable role-based access control for different user levels. The project will also incorporate a
cart system for customers to purchase products and a delivery management system to track orders.

2. Scope:
The project scope encompasses the development of a fully functional E-commerce website with the
following key features:
• Pharmacy Product Management
• Inventory Management
• Role-Based Access Control
• Customer Cart System
• Order Management
• Delivery Management
• Performance Optimization
• Authorization and Authentication

3. Project Requirements Overview
The project requirements include:
• Loading an extensive medicines database
• Enabling pharmacy shops to add custom products
• Allowing shop owners to request additions to the main product database
• Managing inventory and product availability
• Implementing four roles: Owner, Admin, Manager, and Staff
• Designing a cart system for customers
• Providing order placement and management functionality
• Creating a delivery status tracking system
• Ensuring performance and optimization
• Implementing JWT-based authorization
• Providing search, API throttling, and caching functionalities
• Including features for delivery personnel and customer ratings

4. System Architecture
Technology Stack
• Database: PostgreSQL
• Backend: Django, Django Rest Frameworrk
• API Authentication: JWT using djangorestframework-simplejwt
• Monitoring: Django Silk or Django Debug Toolbar
• Other Packages: Autoslugfield, versatileimagefield, drf_spectacular, axesDatabase Design
The database will consist of multiple tables, including:
• Users (Shop owners, Admins, Managers, Staff, Customers)
• Products (Medicines and custom products)
• Inventory (Shop-specific inventory)
• Orders (Customer orders and their details)
• DeliveryStatus (Delivery tracking)
Note: Provide ER diagrams or database schema for a visual representation.

5. Pharmacy Product Management
Loading Medicines Database
• Implement a script to load a comprehensive medicines database.
• Pharmacists can inherit products into their inventory.
Adding Custom Products
• Pharmacy shop owners/admin/staff can add custom products if not in the database.
Requesting Product Addition
• Shop owners can request superusers to add their custom products to the main database.

6. Inventory Management
Shop-Specific Inventory
• Each shop can manage its product inventory and track quantities available.
Product Availability
• Customers can only purchase products that are in stock.
Stock Management
• Implement stock tracking mechanisms to update product quantities.

7. Role-Based Access Control
Roles and Permissions
• Define roles: Owner, Admin, Manager, Staff, Customer.
• Assign specific permissions to each role.
Role Hierarchy• Establish a hierarchy where higher roles have broader permissions.
Creating Assistants
• Shop owners and admins can create assistants with roles like manager or staff.

8. Customer Cart System
Adding Products to Cart
• Allow customers to add multiple products to their cart.
Cart Price Calculation
• Display the current product price in the cart.

9. Order Management
Placing Orders
• Customers can place orders, and order details are stored.
Order Constraints
• Once an order is placed, the product price and delivery address cannot be changed.
Stock-Out Handling
• Orders fail if a product is out of stock, and customers are notified.

10. Delivery Management
Delivery Status Tracking
• Implement a system to track delivery status.
Delivery Status Update
• All roles can update the delivery status, and only Admin/Owner can undo the completed status.
Completion and Undoing
• Completed delivery status can be undone only by Admin/Owner.

11. Performance and Optimization
Pagination
• Utilize pagination to handle large datasets efficiently.
Response Time Limits
• Queries should not exceed 350ms response time.
Query Monitoring and Optimization
• Use Django Silk or Debug Toolbar to monitor and optimize queries.• Implement annotate and eager loading to minimize query count.

12. Authorization and Authentication
JWT-based Authorization
• Implement JWT-based authorization for secure API endpoints.
Custom Authorization
• Develop custom authorization for role-based access.
Secure API Endpoints
• Define public (read-only) and private (read+write) endpoints with appropriate permissions.

13. Additional Features
Search Functionality
• Implement search endpoints for customers and products.
API Throttling
• Apply API throttling to prevent excessive requests.
Caching
• Implement caching to reduce database load.
Delivery Man Features
• Delivery personnel can view assigned tasks and earnings for the month.
Customer Rating System
• Allow customers to rate deliveries on a 1-5 star scale.

14. Conclusion
Project Completion
Upon successful implementation of the above features, the E-commerce Pharmacy Website (Backend) will be ready
for deployment.
Future Enhancements
• Provide user feedback and rating mechanisms.
• Integrate with payment gateways.
• Enhance user interface and experience.
• Explore additional features based on user feedback.This comprehensive project documentation outlines the objectives, scope, requirements, architecture,
and key functionalities of the E-commerce Pharmacy Website intern project. It serves as a roadmap for
the development process and guides project stakeholders throughout its lifecycle.
