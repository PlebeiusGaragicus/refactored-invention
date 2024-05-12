import datetime
import time

import streamlit as st


def cmp_header():
    st.title(":rainbow[PlebChat] 🗣️🤖💬")
    st.header("", divider="rainbow")



class Post:
    def __init__(self, body: str, user=None, config: dict = None):
        self.body = body
        self.user = user
        # self.datetime = datetime.datetime.now()
        self.datetime = datetime.datetime.fromtimestamp(time.time()).strftime('%B %d `%y - %H:%M:%S')
        
        self.parameters = config or {}

        self.children = []
        self.show_children = True

class Thread(Post):
    def __init__(self, title: str, body: str, topics=None, conversational_goals=None, user=None):
        super().__init__(body=body, user=user)
        self.title = title
        self.topics = topics or []
        self.conversational_goals = conversational_goals or []




def process_post(parent: Post, body: str, user=None, config=None):
    if body.strip():  # Only add post if there's actual content
        post = Post(body=body, user=user, config=config)
        parent.children.append(post)





















def cmp_thread_head():
    if "thread" not in st.session_state:
        st.session_state.thread = Thread(title="Summer goals", body="I've recently been thinking about what I'm going to do this summer. Any ideas?", user="satoshi")

    st.header(st.session_state.thread.title)
    st.caption(st.session_state.thread.body)
    if st.session_state.thread.user:
        st.caption(f"Posted by: `{st.session_state.thread.user}`")
    if st.session_state.thread.topics:
        st.caption(f"Topics: {st.session_state.thread.topics}")
    if st.session_state.thread.conversational_goals:
        st.caption(f"Conversational Goals: {st.session_state.thread.conversational_goals}")

    st.markdown("---")


def cmp_reply_form(post: Post, indent=0, top_level=False):
    if top_level:
        # cols = st.columns((indent, 1))
        cols = st.columns((1, 1))
        reply_text = "Reply to post"
    else:
        cols = st.columns((1))
        reply_text = "Reply"

    with cols[-1]:
        with st.popover(reply_text, use_container_width=True):
            with st.form(f"reply_form_{id(post)}", clear_on_submit=True):  # Unique form ID for each post
                # st.text_area("Reply:", key=f"reply_{id(post)}")
                st.text_area("Reply:", key=f"reply_{id(post)}", label_visibility="collapsed")
                config = {
                    "annotate": st.checkbox("Annotate", key=f"annotate_{id(post)}"),
                }
                if st.form_submit_button("Submit"):
                    reply_text = st.session_state[f"reply_{id(post)}"]
                    process_post(post, body=reply_text, user="satoshi", config=config)
                    st.rerun()


def cmp_posts(post: Post):
    if post.children:
        if post != st.session_state.thread:
            show_button_text = "Hide replies" if post.show_children else "Show replies"
            if st.button(show_button_text, key=id(post)):
                post.show_children = not post.show_children
                st.rerun()

        if post.show_children:
            for child in post.children:
                with st.container(border=True):
                    cols = st.columns((4, 1))
                    with cols[0]:
                        # cols3 = st.columns((1, 1))
                        # with cols3[0]:
                            # if child.user:
                        by_line = f"by: `{child.user if child.user else "anon"}`"
                            # st.caption(f"by: `{child.user}`")
                        by_line += f" | {child.datetime}"

                        st.caption(by_line)
                        # with cols3[1]:
                            # st.caption(f"{child.datetime}")
                        st.write(child.body)
                        with st.popover("config"):
                            st.write(child.parameters)
                    with cols[1]:
                        cmp_reply_form(child)  # Render reply form for each post

                    cmp_posts(child)



def main():
    cmp_header()
    cmp_thread_head()

    cmp_reply_form(st.session_state.thread, top_level=True)  # Reply form for the main thread
    cmp_posts(st.session_state.thread)


if __name__ == "__main__":
    main()




















# def cmp_posts(post: Post, indent=0):
#     if post.children:
#         if post.show_children:
#             for child in post.children:
#                 with st.container(border=True):
#                     # st.markdown("---")
#                     cols = st.columns((4, 1))
#                     with cols[0]:
#                         st.write(' ' * indent + child.body)
#                         if child.user:
#                             st.caption(' ' * indent + f"Posted by: `{child.user}`")
#                     with cols[1]:
#                         render_reply_form(child, indent)  # Render reply form for each post

#                         if post.show_children:
#                             if st.button("Hide replies", key=id(post)):
#                                 child.show_children = False
#                                 st.rerun()
#                         else:
#                             if st.button("Show replies", key=id(post)):
#                                 child.show_children = True
#                                 st.rerun()

#                     cmp_posts(child, indent + 4)  # Recursively display replies, increasing indent
#         # else:
#         #     st.write("Show replies")
#         #     if st.button("Show replies", key=id(post)):
#         #         post.show_children = True
#         #         st.rerun()



    # with st.container(border=True):
    #     if st.button("Reply to thread"):
    #         with st.form("reply_form"):
    #             st.text_area("Reply to thread", key="reply")
    #             if st.form_submit_button("Submit"):
    #                 process_post(st.session_state.thread, user="satoshi")
    #                 st.rerun()

    # if st.button("Reply to thread"):
    # with st.form("reply_form", clear_on_submit=True):
    #     reply = st.text_area("Reply to thread", key="reply")
    #     if st.form_submit_button("Submit"):
    #         process_post(st.session_state.thread, body=reply, user="satoshi")
    #         st.rerun()
    # render_reply_form(st.session_state.thread, top_level=True)  # Reply form for the main thread

    # cmp_posts(st.session_state.thread)


        # cols2 = st.columns((4, 1))
        # with cols2[1]:
        #     with st.popover("Reply", use_container_width=True):
        #         st.write("Reply to thread")
        # with cols2[0]:
        #     st.chat_input("Reply to thread", key="reply", on_submit=process_post, args=(st.session_state.thread))


