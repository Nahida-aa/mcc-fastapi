from sqlmodel import Session, select
from server.crud.base_crud import CRUDBase
from server.models.links_model import LinkUserFollow
from server.models.user_model import User


class CRUDLinkUserFollow(CRUDBase[LinkUserFollow,LinkUserFollow,LinkUserFollow]):
    def follow(self, *, follower: User, followed: User, db_session: Session):
        link_follow = LinkUserFollow(follower_id=follower.id, followed_id=followed.id)
        # follower.following_links.append(link_follow)
        # followed.follower_links.append(link_follow)

        # link_follow = LinkUserFollow(follower=follower, followed=followed)# 这种写法会将 follower 和 followed 对象直接传递给 LinkUserFollow 构造函数，这可能会导致 SQLAlchemy 尝试创建新的 User 实例，尤其是在 follower 和 followed 对象没有正确绑定到当前会话的情况下
        db_session.add(link_follow)
        follower.following_count += 1
        followed.followers_count += 1
        db_session.add(follower)
        db_session.add(followed)
        db_session.commit()  # 提交事务
        return followed # 返回被关注者 因为被关注者的粉丝数增加了, 需要显示给关注行为的发起者

    def unfollow(self, *, follower: User, followed: User, db_session: Session):
        # link_follow = next((f for f in follower.following_links if f.followed_id == followed.id), None)
        
        # link_follow = db_session.query(LinkUserFollow).filter_by(follower_id=follower.id, followed_id=followed.id).first()
        statement = select(LinkUserFollow).where(LinkUserFollow.follower_id == follower.id).where(LinkUserFollow.followed_id == followed.id)
        link_follow = db_session.exec(statement).one_or_none()
        if link_follow:
            # follower.following_links.remove(link_follow)
            # followed.follower_links.remove(link_follow)
            db_session.delete(link_follow)
            follower.following_count -= 1
            followed.followers_count -= 1
            db_session.add(follower)
            db_session.add(followed)
            db_session.commit()  # 提交事务
        return followed # 返回被关注者 因为被关注者的粉丝数减少了, 需要显示给取消关注行为的发起者

link_user_follow = CRUDLinkUserFollow(LinkUserFollow)
        