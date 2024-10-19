@Entity
@Table(name="user_feed")
public class User implements Serializable {

    @Id
    @Column(name="user_id")
    private long mUserId;

    @Column(name="is_repost")
    private boolean mIsRepost;

    @Column(name="date_created")
    private Date mDateCreated;

    @OneToOne
    @JoinColumn(name="amici")
    private Friend amici;

}