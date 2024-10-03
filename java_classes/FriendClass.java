@Entity
@Table(name="friend")
public class Friend implements Serializable {

    @Id
    @Column(name="user_id")
    private long mUserId;

    @Column(name="is_repost")
    private boolean m_repost;

    @Column(name="date_created")
    private Date mDateCreated;


}