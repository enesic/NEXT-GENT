--
-- PostgreSQL database dump
--

\restrict 8IRcJcb1iJZ14VKs8QcNtEuw3f9hfFTt8ws1fNjVaw0KRbXtHKKioxsqZ4xpR2h

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: call_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.call_status AS ENUM (
    'IN_PROGRESS',
    'RESOLVED_AI',
    'TRANSFERRED_HUMAN',
    'FAILED',
    'COMPLETED'
);


--
-- Name: customer_segment; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.customer_segment AS ENUM (
    'VIP',
    'GOLD',
    'SILVER',
    'BRONZE',
    'REGULAR'
);


--
-- Name: customer_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.customer_status AS ENUM (
    'ACTIVE',
    'INACTIVE',
    'BLOCKED',
    'DEBT'
);


--
-- Name: interaction_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.interaction_status AS ENUM (
    'PENDING',
    'CONFIRMED',
    'CANCELLED',
    'COMPLETED'
);


--
-- Name: satisfaction_channel; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.satisfaction_channel AS ENUM (
    'EMAIL',
    'SMS',
    'IN_APP',
    'CALL',
    'CHAT'
);


--
-- Name: satisfaction_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.satisfaction_type AS ENUM (
    'NPS',
    'CSAT',
    'CUSTOM'
);


--
-- Name: webhook_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.webhook_status AS ENUM (
    'PENDING',
    'FAILED',
    'RETRYING',
    'MANUALLY_SENT'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_users (
    username character varying NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    role character varying NOT NULL,
    is_active boolean NOT NULL,
    is_super_admin boolean NOT NULL,
    permissions jsonb,
    last_login_at timestamp with time zone,
    login_count integer NOT NULL,
    last_ip character varying,
    two_factor_secret character varying,
    two_factor_enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_logs (
    action_type character varying NOT NULL,
    resource_type character varying NOT NULL,
    resource_id_hash character varying,
    admin_user_id character varying,
    ip_address character varying,
    user_agent character varying,
    changes jsonb,
    retention_until timestamp with time zone NOT NULL,
    is_visible boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: cards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cards (
    name character varying NOT NULL,
    display_name character varying NOT NULL,
    tier_level integer NOT NULL,
    monthly_price numeric(10,2) NOT NULL,
    annual_price numeric(10,2),
    features jsonb NOT NULL,
    max_users integer,
    max_calls_per_month integer,
    max_tokens_per_month integer,
    is_active boolean NOT NULL,
    is_popular boolean NOT NULL,
    description character varying,
    color_primary character varying,
    color_accent character varying,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customers (
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(100) NOT NULL,
    phone_hash character varying(64) NOT NULL,
    customer_id character varying(20),
    pin_hash character varying(255),
    address text,
    city character varying(100),
    country character varying(100),
    postal_code character varying(20),
    segment public.customer_segment NOT NULL,
    status public.customer_status NOT NULL,
    total_orders integer NOT NULL,
    total_spent numeric(10,2) NOT NULL,
    lifetime_value numeric(10,2) NOT NULL,
    debt_amount numeric(10,2) NOT NULL,
    last_order_date timestamp without time zone,
    last_contact_date timestamp without time zone,
    notes text,
    referral_code character varying(50),
    referred_by character varying(50),
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documents (
    filename character varying(255) NOT NULL,
    file_url character varying(512),
    file_type character varying(100) NOT NULL,
    size integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: failed_webhooks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.failed_webhooks (
    event_type character varying(100) NOT NULL,
    webhook_url character varying(500) NOT NULL,
    payload json NOT NULL,
    status public.webhook_status NOT NULL,
    attempts integer NOT NULL,
    last_error text,
    last_status_code integer,
    last_attempt_at timestamp without time zone,
    related_entity_type character varying(50),
    related_entity_id character varying(100),
    manually_retried_at timestamp without time zone,
    manually_retried_by character varying(100),
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: flow_executions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.flow_executions (
    flow_id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    status character varying NOT NULL,
    input_data jsonb,
    output_data jsonb,
    error_message text,
    error_stack text,
    execution_time_ms integer,
    executed_actions jsonb,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: flows; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.flows (
    tenant_id uuid NOT NULL,
    name character varying NOT NULL,
    description text,
    config jsonb NOT NULL,
    is_active boolean NOT NULL,
    is_template boolean NOT NULL,
    total_executions integer NOT NULL,
    successful_executions integer NOT NULL,
    failed_executions integer NOT NULL,
    priority integer NOT NULL,
    category character varying,
    tags jsonb,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: interactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interactions (
    title character varying(255) NOT NULL,
    description text,
    type character varying(50) NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    client_name character varying(255) NOT NULL,
    client_email character varying(255) NOT NULL,
    client_phone character varying(50),
    status public.interaction_status NOT NULL,
    meta_data jsonb,
    google_calendar_event_id character varying(255),
    version integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: satisfactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.satisfactions (
    customer_id character varying,
    interaction_id character varying,
    call_id character varying,
    survey_type public.satisfaction_type NOT NULL,
    channel public.satisfaction_channel NOT NULL,
    nps_score integer,
    csat_score integer,
    custom_rating double precision,
    feedback_text text,
    sentiment character varying(20),
    sentiment_score double precision,
    ai_summary text,
    responded_at timestamp without time zone,
    survey_sent_at timestamp without time zone,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: subscription_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscription_plans (
    tenant_id uuid NOT NULL,
    card_id uuid NOT NULL,
    status character varying NOT NULL,
    billing_cycle character varying NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    trial_end_date timestamp without time zone,
    next_billing_date timestamp without time zone,
    current_users integer NOT NULL,
    current_calls_this_month integer NOT NULL,
    current_tokens_this_month integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    currency character varying NOT NULL,
    config jsonb,
    cancelled_at timestamp without time zone,
    cancellation_reason character varying,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tenants (
    name character varying NOT NULL,
    slug character varying NOT NULL,
    domain character varying,
    is_active boolean NOT NULL,
    config jsonb,
    webhook_url character varying,
    system_prompt character varying,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: token_usage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.token_usage (
    call_id character varying,
    tenant_id character varying,
    model_name character varying NOT NULL,
    tokens_prompt integer NOT NULL,
    tokens_completion integer NOT NULL,
    total_tokens integer NOT NULL,
    estimated_cost double precision NOT NULL,
    call_duration_seconds double precision,
    success boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: vapi_calls; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vapi_calls (
    vapi_call_id character varying(255) NOT NULL,
    caller_name_encrypted text,
    caller_phone_encrypted text NOT NULL,
    transcript_encrypted text,
    phone_hash character varying(64) NOT NULL,
    call_duration_seconds integer NOT NULL,
    call_status public.call_status NOT NULL,
    resolution_type character varying(100),
    ai_confidence_score double precision,
    transferred_at timestamp without time zone,
    agent_id character varying(255),
    transfer_reason text,
    started_at timestamp without time zone NOT NULL,
    ended_at timestamp without time zone,
    customer_id character varying(255),
    sentiment character varying(20),
    sentiment_score double precision,
    call_quality_score integer,
    notes_encrypted text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tenant_id uuid NOT NULL
);


--
-- Name: admin_users admin_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: cards cards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: customers customers_referral_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_referral_code_key UNIQUE (referral_code);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: failed_webhooks failed_webhooks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.failed_webhooks
    ADD CONSTRAINT failed_webhooks_pkey PRIMARY KEY (id);


--
-- Name: flow_executions flow_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flow_executions
    ADD CONSTRAINT flow_executions_pkey PRIMARY KEY (id);


--
-- Name: flows flows_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flows
    ADD CONSTRAINT flows_pkey PRIMARY KEY (id);


--
-- Name: interactions interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interactions
    ADD CONSTRAINT interactions_pkey PRIMARY KEY (id);


--
-- Name: satisfactions satisfactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.satisfactions
    ADD CONSTRAINT satisfactions_pkey PRIMARY KEY (id);


--
-- Name: subscription_plans subscription_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_pkey PRIMARY KEY (id);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: token_usage token_usage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_usage
    ADD CONSTRAINT token_usage_pkey PRIMARY KEY (id);


--
-- Name: vapi_calls vapi_calls_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vapi_calls
    ADD CONSTRAINT vapi_calls_pkey PRIMARY KEY (id);


--
-- Name: admin_users_email_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX admin_users_email_idx ON public.admin_users USING btree (email);


--
-- Name: admin_users_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX admin_users_id_idx ON public.admin_users USING btree (id);


--
-- Name: admin_users_username_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX admin_users_username_idx ON public.admin_users USING btree (username);


--
-- Name: audit_logs_action_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_action_type_idx ON public.audit_logs USING btree (action_type);


--
-- Name: audit_logs_admin_user_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_admin_user_id_idx ON public.audit_logs USING btree (admin_user_id);


--
-- Name: audit_logs_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_id_idx ON public.audit_logs USING btree (id);


--
-- Name: audit_logs_resource_id_hash_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_resource_id_hash_idx ON public.audit_logs USING btree (resource_id_hash);


--
-- Name: audit_logs_resource_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_resource_type_idx ON public.audit_logs USING btree (resource_type);


--
-- Name: cards_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cards_id_idx ON public.cards USING btree (id);


--
-- Name: customers_customer_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX customers_customer_id_idx ON public.customers USING btree (customer_id);


--
-- Name: customers_email_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX customers_email_idx ON public.customers USING btree (email);


--
-- Name: customers_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX customers_id_idx ON public.customers USING btree (id);


--
-- Name: customers_phone_hash_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX customers_phone_hash_idx ON public.customers USING btree (phone_hash);


--
-- Name: customers_segment_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX customers_segment_idx ON public.customers USING btree (segment);


--
-- Name: customers_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX customers_status_idx ON public.customers USING btree (status);


--
-- Name: customers_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX customers_tenant_id_idx ON public.customers USING btree (tenant_id);


--
-- Name: documents_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_id_idx ON public.documents USING btree (id);


--
-- Name: documents_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_tenant_id_idx ON public.documents USING btree (tenant_id);


--
-- Name: failed_webhooks_event_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_webhooks_event_type_idx ON public.failed_webhooks USING btree (event_type);


--
-- Name: failed_webhooks_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_webhooks_id_idx ON public.failed_webhooks USING btree (id);


--
-- Name: failed_webhooks_related_entity_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_webhooks_related_entity_id_idx ON public.failed_webhooks USING btree (related_entity_id);


--
-- Name: failed_webhooks_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_webhooks_status_idx ON public.failed_webhooks USING btree (status);


--
-- Name: failed_webhooks_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_webhooks_tenant_id_idx ON public.failed_webhooks USING btree (tenant_id);


--
-- Name: flow_executions_flow_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flow_executions_flow_id_idx ON public.flow_executions USING btree (flow_id);


--
-- Name: flow_executions_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flow_executions_id_idx ON public.flow_executions USING btree (id);


--
-- Name: flow_executions_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flow_executions_tenant_id_idx ON public.flow_executions USING btree (tenant_id);


--
-- Name: flows_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flows_id_idx ON public.flows USING btree (id);


--
-- Name: flows_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flows_name_idx ON public.flows USING btree (name);


--
-- Name: flows_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flows_tenant_id_idx ON public.flows USING btree (tenant_id);


--
-- Name: idx_audit_admin_action; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_admin_action ON public.audit_logs USING btree (admin_user_id, action_type);


--
-- Name: idx_audit_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_created_at ON public.audit_logs USING btree (created_at);


--
-- Name: idx_audit_retention; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_audit_retention ON public.audit_logs USING btree (retention_until);


--
-- Name: idx_interactions_no_overlap; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX idx_interactions_no_overlap ON public.interactions USING btree (tenant_id, start_time, end_time) WHERE (status = ANY (ARRAY['PENDING'::public.interaction_status, 'CONFIRMED'::public.interaction_status]));


--
-- Name: idx_token_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_token_created_at ON public.token_usage USING btree (created_at);


--
-- Name: idx_token_model; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_token_model ON public.token_usage USING btree (model_name, created_at);


--
-- Name: idx_token_tenant_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_token_tenant_date ON public.token_usage USING btree (tenant_id, created_at);


--
-- Name: interactions_end_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interactions_end_time_idx ON public.interactions USING btree (end_time);


--
-- Name: interactions_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interactions_id_idx ON public.interactions USING btree (id);


--
-- Name: interactions_start_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interactions_start_time_idx ON public.interactions USING btree (start_time);


--
-- Name: interactions_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interactions_tenant_id_idx ON public.interactions USING btree (tenant_id);


--
-- Name: interactions_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interactions_type_idx ON public.interactions USING btree (type);


--
-- Name: satisfactions_call_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX satisfactions_call_id_idx ON public.satisfactions USING btree (call_id);


--
-- Name: satisfactions_customer_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX satisfactions_customer_id_idx ON public.satisfactions USING btree (customer_id);


--
-- Name: satisfactions_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX satisfactions_id_idx ON public.satisfactions USING btree (id);


--
-- Name: satisfactions_interaction_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX satisfactions_interaction_id_idx ON public.satisfactions USING btree (interaction_id);


--
-- Name: satisfactions_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX satisfactions_tenant_id_idx ON public.satisfactions USING btree (tenant_id);


--
-- Name: subscription_plans_card_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX subscription_plans_card_id_idx ON public.subscription_plans USING btree (card_id);


--
-- Name: subscription_plans_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX subscription_plans_id_idx ON public.subscription_plans USING btree (id);


--
-- Name: subscription_plans_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX subscription_plans_tenant_id_idx ON public.subscription_plans USING btree (tenant_id);


--
-- Name: tenants_domain_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX tenants_domain_idx ON public.tenants USING btree (domain);


--
-- Name: tenants_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tenants_id_idx ON public.tenants USING btree (id);


--
-- Name: tenants_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tenants_name_idx ON public.tenants USING btree (name);


--
-- Name: tenants_slug_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX tenants_slug_idx ON public.tenants USING btree (slug);


--
-- Name: token_usage_call_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_usage_call_id_idx ON public.token_usage USING btree (call_id);


--
-- Name: token_usage_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_usage_id_idx ON public.token_usage USING btree (id);


--
-- Name: token_usage_model_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_usage_model_name_idx ON public.token_usage USING btree (model_name);


--
-- Name: token_usage_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_usage_tenant_id_idx ON public.token_usage USING btree (tenant_id);


--
-- Name: vapi_calls_call_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vapi_calls_call_status_idx ON public.vapi_calls USING btree (call_status);


--
-- Name: vapi_calls_customer_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vapi_calls_customer_id_idx ON public.vapi_calls USING btree (customer_id);


--
-- Name: vapi_calls_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vapi_calls_id_idx ON public.vapi_calls USING btree (id);


--
-- Name: vapi_calls_phone_hash_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vapi_calls_phone_hash_idx ON public.vapi_calls USING btree (phone_hash);


--
-- Name: vapi_calls_tenant_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vapi_calls_tenant_id_idx ON public.vapi_calls USING btree (tenant_id);


--
-- Name: vapi_calls_vapi_call_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX vapi_calls_vapi_call_id_idx ON public.vapi_calls USING btree (vapi_call_id);


--
-- Name: flow_executions flow_executions_flow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flow_executions
    ADD CONSTRAINT flow_executions_flow_id_fkey FOREIGN KEY (flow_id) REFERENCES public.flows(id);


--
-- Name: flow_executions flow_executions_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flow_executions
    ADD CONSTRAINT flow_executions_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: flows flows_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flows
    ADD CONSTRAINT flows_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: subscription_plans subscription_plans_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_card_id_fkey FOREIGN KEY (card_id) REFERENCES public.cards(id);


--
-- Name: subscription_plans subscription_plans_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 8IRcJcb1iJZ14VKs8QcNtEuw3f9hfFTt8ws1fNjVaw0KRbXtHKKioxsqZ4xpR2h

