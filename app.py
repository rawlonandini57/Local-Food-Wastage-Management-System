import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from database import init_db, run_query, execute_dml, QUERIES

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🍽️ Food Waste Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-left: 4px solid #2E7D32;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1B5E20;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─── Init ─────────────────────────────────────────────────────────────────────
init_db()

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🍽️ Local Food Wastage Management System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Connecting surplus food providers with those in need · Powered by SQL & Streamlit</div>', unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/food-bank.png", width=80)
    st.title("Navigation")
    page = st.radio("", [
        "📊 Dashboard",
        "🔍 SQL Queries",
        "🗺️ Explore Data",
        "✏️ CRUD Operations",
    ], label_visibility="collapsed")

    st.divider()
    stats = run_query("SELECT COUNT(*) as n FROM providers").iloc[0, 0]
    st.metric("Total Providers", stats)
    stats2 = run_query("SELECT COUNT(*) as n FROM receivers").iloc[0, 0]
    st.metric("Total Receivers", stats2)
    stats3 = run_query("SELECT COUNT(*) as n FROM food_listings").iloc[0, 0]
    st.metric("Food Listings", stats3)
    stats4 = run_query("SELECT COUNT(*) as n FROM claims").iloc[0, 0]
    st.metric("Total Claims", stats4)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

    total_qty   = run_query("SELECT SUM(Quantity) FROM food_listings").iloc[0, 0]
    completed   = run_query("SELECT COUNT(*) FROM claims WHERE Status='Completed'").iloc[0, 0]
    pending     = run_query("SELECT COUNT(*) FROM claims WHERE Status='Pending'").iloc[0, 0]
    cancelled   = run_query("SELECT COUNT(*) FROM claims WHERE Status='Cancelled'").iloc[0, 0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🥗 Total Food (units)", f"{total_qty:,}")
    c2.metric("✅ Completed Claims", completed)
    c3.metric("⏳ Pending Claims", pending)
    c4.metric("❌ Cancelled Claims", cancelled)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Provider Types</div>', unsafe_allow_html=True)
        df = run_query(QUERIES["Q2: Provider Type with Most Food Listings"])
        fig = px.pie(df, names="Provider_Type", values="total_quantity",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     hole=0.4)
        fig.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Claim Status Breakdown</div>', unsafe_allow_html=True)
        df2 = run_query(QUERIES["Q10: Claim Status Breakdown (%)"])
        fig2 = px.bar(df2, x="Status", y="percentage",
                      color="Status",
                      color_discrete_map={"Completed": "#4CAF50", "Pending": "#FFC107", "Cancelled": "#F44336"},
                      text="percentage")
        fig2.update_traces(texttemplate="%{text}%", textposition="outside")
        fig2.update_layout(showlegend=False, margin=dict(t=10, b=10), yaxis_title="Percentage (%)")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Food Types Distribution</div>', unsafe_allow_html=True)
        df3 = run_query(QUERIES["Q7: Most Commonly Available Food Types"])
        fig3 = px.bar(df3, x="Food_Type", y="total_quantity",
                      color="Food_Type",
                      color_discrete_sequence=["#66BB6A", "#42A5F5", "#FFA726"])
        fig3.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Meal Type Claims</div>', unsafe_allow_html=True)
        df4 = run_query(QUERIES["Q12: Most Claimed Meal Type"])
        fig4 = px.bar(df4, x="Meal_Type", y="total_claims",
                      color="Meal_Type",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig4.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Top 10 Cities by Food Listings</div>', unsafe_allow_html=True)
    df5 = run_query(QUERIES["Q6: City with Highest Number of Food Listings"]).head(10)
    fig5 = px.bar(df5, x="city", y="listing_count",
                  color="total_quantity", color_continuous_scale="Greens",
                  labels={"listing_count": "Listings", "city": "City"})
    fig5.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: SQL QUERIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 SQL Queries":
    st.markdown('<div class="section-header">15 SQL Queries & Analysis</div>', unsafe_allow_html=True)

    query_name = st.selectbox("Select a query to run:", list(QUERIES.keys()))

    if query_name:
        with st.expander("📝 View SQL", expanded=False):
            st.code(QUERIES[query_name].strip(), language="sql")

        df = run_query(QUERIES[query_name])

        if df.empty:
            st.info("No data returned for this query (e.g. no items expiring in the next 30 days based on dataset dates).")
        else:
            st.success(f"✅ {len(df)} rows returned")
            st.dataframe(df, use_container_width=True, height=400)

            # Auto chart for numeric queries
            num_cols = df.select_dtypes(include="number").columns.tolist()
            str_cols = df.select_dtypes(include="object").columns.tolist()
            if num_cols and str_cols:
                col_x = str_cols[0]
                col_y = st.selectbox("Chart Y-axis:", num_cols)
                chart_type = st.radio("Chart type:", ["Bar", "Line", "Scatter"], horizontal=True)
                if chart_type == "Bar":
                    fig = px.bar(df.head(20), x=col_x, y=col_y, color_discrete_sequence=["#4CAF50"])
                elif chart_type == "Line":
                    fig = px.line(df.head(20), x=col_x, y=col_y, markers=True, color_discrete_sequence=["#4CAF50"])
                else:
                    fig = px.scatter(df.head(20), x=col_x, y=col_y, color_discrete_sequence=["#4CAF50"])
                st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, f"{query_name[:30]}.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: EXPLORE DATA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Explore Data":
    st.markdown('<div class="section-header">Explore & Filter Data</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🏪 Providers", "👥 Receivers", "🍱 Food Listings", "📋 Claims"])

    # ── Providers ──
    with tab1:
        df_p = run_query("SELECT * FROM providers")
        cities_p = ["All"] + sorted(df_p["City"].dropna().unique().tolist())
        types_p  = ["All"] + sorted(df_p["Type"].dropna().unique().tolist())
        c1, c2 = st.columns(2)
        sel_city = c1.selectbox("Filter by City", cities_p, key="p_city")
        sel_type = c2.selectbox("Filter by Type", types_p, key="p_type")

        mask = pd.Series([True] * len(df_p))
        if sel_city != "All": mask &= df_p["City"] == sel_city
        if sel_type != "All": mask &= df_p["Type"] == sel_type
        filtered = df_p[mask]
        st.info(f"Showing {len(filtered)} providers")
        st.dataframe(filtered, use_container_width=True, height=400)

    # ── Receivers ──
    with tab2:
        df_r = run_query("SELECT * FROM receivers")
        cities_r = ["All"] + sorted(df_r["City"].dropna().unique().tolist())
        types_r  = ["All"] + sorted(df_r["Type"].dropna().unique().tolist())
        c1, c2 = st.columns(2)
        sel_city_r = c1.selectbox("Filter by City", cities_r, key="r_city")
        sel_type_r = c2.selectbox("Filter by Type", types_r, key="r_type")

        mask_r = pd.Series([True] * len(df_r))
        if sel_city_r != "All": mask_r &= df_r["City"] == sel_city_r
        if sel_type_r != "All": mask_r &= df_r["Type"] == sel_type_r
        filtered_r = df_r[mask_r]
        st.info(f"Showing {len(filtered_r)} receivers")
        st.dataframe(filtered_r, use_container_width=True, height=400)

    # ── Food Listings ──
    with tab3:
        df_f = run_query("SELECT * FROM food_listings")
        c1, c2, c3 = st.columns(3)
        cities_f   = ["All"] + sorted(df_f["Location"].dropna().unique().tolist())
        food_types = ["All"] + sorted(df_f["Food_Type"].dropna().unique().tolist())
        meal_types = ["All"] + sorted(df_f["Meal_Type"].dropna().unique().tolist())
        prov_types = ["All"] + sorted(df_f["Provider_Type"].dropna().unique().tolist())

        sel_loc  = c1.selectbox("City / Location", cities_f, key="f_city")
        sel_ft   = c2.selectbox("Food Type", food_types, key="f_ft")
        sel_mt   = c3.selectbox("Meal Type", meal_types, key="f_mt")
        sel_pt   = st.selectbox("Provider Type", prov_types, key="f_pt")

        mask_f = pd.Series([True] * len(df_f))
        if sel_loc != "All": mask_f &= df_f["Location"] == sel_loc
        if sel_ft  != "All": mask_f &= df_f["Food_Type"] == sel_ft
        if sel_mt  != "All": mask_f &= df_f["Meal_Type"] == sel_mt
        if sel_pt  != "All": mask_f &= df_f["Provider_Type"] == sel_pt
        filtered_f = df_f[mask_f]

        st.info(f"Showing {len(filtered_f)} food listings · Total quantity: {filtered_f['Quantity'].sum():,}")
        st.dataframe(filtered_f, use_container_width=True, height=400)

        if not filtered_f.empty:
            csv_f = filtered_f.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download filtered listings", csv_f, "filtered_food_listings.csv")

    # ── Claims ──
    with tab4:
        df_c = run_query("""
            SELECT c.Claim_ID, fl.Food_Name, fl.Food_Type, fl.Meal_Type,
                   r.Name AS Receiver_Name, r.Type AS Receiver_Type, r.City,
                   r.Contact, c.Status, c.Timestamp
            FROM claims c
            JOIN food_listings fl ON c.Food_ID = fl.Food_ID
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        """)
        statuses = ["All"] + sorted(df_c["Status"].dropna().unique().tolist())
        c1, c2 = st.columns(2)
        sel_st   = c1.selectbox("Filter by Status", statuses, key="c_status")
        search_r = c2.text_input("Search Receiver Name", key="c_recv")

        mask_c = pd.Series([True] * len(df_c))
        if sel_st != "All": mask_c &= df_c["Status"] == sel_st
        if search_r: mask_c &= df_c["Receiver_Name"].str.contains(search_r, case=False, na=False)
        filtered_c = df_c[mask_c]

        st.info(f"Showing {len(filtered_c)} claims")
        st.dataframe(filtered_c, use_container_width=True, height=400)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: CRUD OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ CRUD Operations":
    st.markdown('<div class="section-header">CRUD Operations</div>', unsafe_allow_html=True)

    crud_tab = st.tabs(["➕ Add Food Listing", "✏️ Update Claim Status", "🗑️ Delete Listing",
                         "➕ Add Provider", "➕ Add Receiver"])

    # ── CREATE: Food Listing ──
    with crud_tab[0]:
        st.subheader("Add New Food Listing")
        providers = run_query("SELECT Provider_ID, Name, Type, City FROM providers ORDER BY Name")

        with st.form("add_food_form"):
            c1, c2 = st.columns(2)
            food_name = c1.text_input("Food Name*")
            quantity  = c2.number_input("Quantity*", min_value=1, value=10)
            expiry    = st.date_input("Expiry Date*")
            prov_opts = providers.apply(lambda r: f"{r['Name']} ({r['Type']}, {r['City']})", axis=1).tolist()
            prov_sel  = st.selectbox("Provider*", prov_opts)
            prov_id   = providers.iloc[prov_opts.index(prov_sel)]["Provider_ID"]
            prov_type = providers.iloc[prov_opts.index(prov_sel)]["Type"]
            location  = providers.iloc[prov_opts.index(prov_sel)]["City"]
            c3, c4    = st.columns(2)
            food_type = c3.selectbox("Food Type*", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = c4.selectbox("Meal Type*", ["Breakfast", "Lunch", "Dinner", "Snacks"])

            if st.form_submit_button("➕ Add Listing", type="primary"):
                if not food_name:
                    st.error("Food Name is required.")
                else:
                    new_id = run_query("SELECT COALESCE(MAX(Food_ID),0)+1 FROM food_listings").iloc[0, 0]
                    sql = """INSERT INTO food_listings
                             (Food_ID,Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type)
                             VALUES (?,?,?,?,?,?,?,?,?)"""
                    execute_dml(sql, (new_id, food_name, quantity, str(expiry), int(prov_id), prov_type, location, food_type, meal_type))
                    st.success(f"✅ Food listing '{food_name}' added with ID {new_id}!")

    # ── UPDATE: Claim Status ──
    with crud_tab[1]:
        st.subheader("Update Claim Status")
        claims_df = run_query("""
            SELECT c.Claim_ID, fl.Food_Name, r.Name AS Receiver, c.Status
            FROM claims c
            JOIN food_listings fl ON c.Food_ID=fl.Food_ID
            JOIN receivers r ON c.Receiver_ID=r.Receiver_ID
            ORDER BY c.Claim_ID DESC LIMIT 100
        """)

        with st.form("update_claim_form"):
            claim_opts = claims_df.apply(
                lambda r: f"#{r['Claim_ID']} · {r['Food_Name']} → {r['Receiver']} [{r['Status']}]", axis=1
            ).tolist()
            sel_claim = st.selectbox("Select Claim", claim_opts)
            claim_id  = claims_df.iloc[claim_opts.index(sel_claim)]["Claim_ID"]
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])

            if st.form_submit_button("✏️ Update Status", type="primary"):
                execute_dml("UPDATE claims SET Status=? WHERE Claim_ID=?", (new_status, int(claim_id)))
                st.success(f"✅ Claim #{claim_id} updated to '{new_status}'!")

    # ── DELETE: Food Listing ──
    with crud_tab[2]:
        st.subheader("Delete Food Listing")
        listings_df = run_query("SELECT Food_ID, Food_Name, Quantity, Location FROM food_listings ORDER BY Food_ID DESC LIMIT 100")

        with st.form("delete_food_form"):
            listing_opts = listings_df.apply(
                lambda r: f"#{r['Food_ID']} · {r['Food_Name']} (qty:{r['Quantity']}, {r['Location']})", axis=1
            ).tolist()
            sel_listing = st.selectbox("Select Food Listing to Delete", listing_opts)
            food_id = listings_df.iloc[listing_opts.index(sel_listing)]["Food_ID"]
            st.warning("⚠️ This will also delete related claims for this listing.")

            if st.form_submit_button("🗑️ Delete Listing", type="primary"):
                execute_dml("DELETE FROM claims WHERE Food_ID=?", (int(food_id),))
                execute_dml("DELETE FROM food_listings WHERE Food_ID=?", (int(food_id),))
                st.success(f"✅ Food listing #{food_id} and its claims deleted!")

    # ── CREATE: Provider ──
    with crud_tab[3]:
        st.subheader("Add New Provider")
        with st.form("add_provider_form"):
            c1, c2 = st.columns(2)
            p_name    = c1.text_input("Provider Name*")
            p_type    = c2.selectbox("Provider Type*", ["Restaurant", "Grocery Store", "Supermarket", "Catering Service"])
            p_address = st.text_area("Address")
            c3, c4    = st.columns(2)
            p_city    = c3.text_input("City*")
            p_contact = c4.text_input("Contact")

            if st.form_submit_button("➕ Add Provider", type="primary"):
                if not p_name or not p_city:
                    st.error("Name and City are required.")
                else:
                    new_pid = run_query("SELECT COALESCE(MAX(Provider_ID),0)+1 FROM providers").iloc[0, 0]
                    execute_dml(
                        "INSERT INTO providers (Provider_ID,Name,Type,Address,City,Contact) VALUES (?,?,?,?,?,?)",
                        (new_pid, p_name, p_type, p_address, p_city, p_contact)
                    )
                    st.success(f"✅ Provider '{p_name}' added with ID {new_pid}!")

    # ── CREATE: Receiver ──
    with crud_tab[4]:
        st.subheader("Add New Receiver")
        with st.form("add_receiver_form"):
            c1, c2 = st.columns(2)
            r_name    = c1.text_input("Receiver Name*")
            r_type    = c2.selectbox("Receiver Type*", ["NGO", "Individual", "Shelter", "Community Center", "Charity"])
            c3, c4    = st.columns(2)
            r_city    = c3.text_input("City*")
            r_contact = c4.text_input("Contact")

            if st.form_submit_button("➕ Add Receiver", type="primary"):
                if not r_name or not r_city:
                    st.error("Name and City are required.")
                else:
                    new_rid = run_query("SELECT COALESCE(MAX(Receiver_ID),0)+1 FROM receivers").iloc[0, 0]
                    execute_dml(
                        "INSERT INTO receivers (Receiver_ID,Name,Type,City,Contact) VALUES (?,?,?,?,?)",
                        (new_rid, r_name, r_type, r_city, r_contact)
                    )
                    st.success(f"✅ Receiver '{r_name}' added with ID {new_rid}!")
