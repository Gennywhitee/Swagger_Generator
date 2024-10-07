@Entity
@Table(name="friend")
public class Friend implements Serializable {

    @Id
    @Column(name="user_id")
    private long mUserId;

    @Column(name="is_repost")
    private boolean mIsRepost;

    @Column(name="date_created")
    private Date mDateCreated;


}